from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm, UploadParamsForm, UploadTicketForm
import mimetypes
from .algorithm import build_questions_from_tex
from .algorithm import doc_parsing, create_pdf, create_texs, create_folder
from .algorithm import get_statistics
from .models import File
from .algorithm import get_minimal_number_of_questions, create_questions_tex

import uuid

import os


def handle_file(f, uuid):
    if not os.path.exists(f'exam_questions/static/upload/{uuid}'):
        os.mkdir(f'exam_questions/static/upload/{uuid}')
    with open(f'exam_questions/static/upload/{uuid}/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    if request.method == 'POST':
        return HttpResponseRedirect(f"{uuid.uuid1()}/load")
    else:
        return render(request, 'index.html')


def statistics(request, uuid, filename):
    if request.method == 'POST':
        return HttpResponseRedirect(f"/exam_questions/{uuid}/params/{filename}")
    else:
        stats = File.objects.filter(filename=filename)[0].stats
        stats['num_of_q']['Задача'] = stats['num_of_q'].pop('6')
    return render(request, 'statistics.html',
                  {'stats': stats['table'], 'density': stats['density'], 'questions': stats['num_of_q']})


def params_for_tickets(request, uuid, filename):
    """TODO(docx)"""
    if request.method == 'POST':
        form = UploadTicketForm(request.POST, request.FILES)
        if form.is_valid():
            obj = File.objects.filter(uuid=uuid)[0]
            obj.tickets = form.cleaned_data['num_problems_in_ticket']
            obj.save()
            obj = File.objects.filter(uuid=uuid)[0]
            filename = obj.filename

            _, file_extension = os.path.splitext(filename)
            if (file_extension == '.docx'):
                questions = create_questions_tex(f"exam_questions/static/upload/{uuid}/", filename, obj.params,
                                                 obj.questions_pool, obj.tickets)
                create_texs(questions, obj.params, f"exam_questions/static/upload/{uuid}/")
                create_pdf(obj.tickets, f"exam_questions/static/upload/{uuid}/")
                if (obj.params['pdf_folder'] == True):
                    create_folder(obj.tickets, f"exam_questions/static/upload/{uuid}/")
            else:
                questions = create_questions_tex(f"exam_questions/static/upload/{uuid}/", filename, obj.params,
                                                 obj.questions_pool, obj.tickets)
                create_texs(questions, obj.params, f"exam_questions/static/upload/{uuid}/")
                create_pdf(obj.tickets, f"exam_questions/static/upload/{uuid}/")
                if (obj.params['pdf_folder'] == True):
                    create_folder(obj.tickets, f"exam_questions/static/upload/{uuid}/")
            if questions == "Error":
                return HttpResponse("Error")
            if obj.output_format == 'PDF':
                return HttpResponseRedirect(f"/exam_questions/{uuid}/preview/tickets.pdf")
            elif obj.output_format == 'TEX':
                return HttpResponseRedirect(f"/exam_questions/{uuid}/preview/tickets.tex")
    else:
        form = UploadTicketForm()
        num = File.objects.filter(uuid=uuid)[0].tickets
        return render(request, 'ticket_suggestion.html', {'form': form, 'num_of_tickets': num})


def load(request, uuid):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_file(request.FILES['file'], uuid)
            filename = request.FILES['file']
            if (form.cleaned_data['additional_file']):
                stats, questions_pool, title = get_statistics(
                    f"exam_questions/static/upload/{uuid}/" + request.FILES['file'].name,
                    "exam_questions/static/upload/" + request.FILES['additional_file'].name)
                handle_file(request.FILES['additional_file'], uuid)
                File(filename=filename, questions_pool=questions_pool, stats=stats, title=title, uuid=uuid).save()
                return HttpResponseRedirect(f"/exam_questions/{uuid}/statistics/{filename}")
            else:
                stats, questions_pool, title = get_statistics(
                    f"exam_questions/static/upload/{uuid}/" + request.FILES['file'].name)
                File(filename=filename, questions_pool=questions_pool, stats=stats, title=title, uuid=uuid).save()
                return HttpResponseRedirect(f"/exam_questions/{uuid}/statistics/{filename}")
    else:
        form = UploadFileForm()
    return render(request, 'load.html', {'form': form})


def params(request, uuid, filename):
    if request.method == 'POST':
        form = UploadParamsForm(request.POST, request.FILES)
        if form.is_valid():
            questions_pool = File.objects.filter(uuid=uuid)[0].questions_pool
            info = {'3': form.cleaned_data['num_questions_3_in_ticket'],
                    '4': form.cleaned_data[
                        'num_questions_4_in_ticket'],
                    '5': form.cleaned_data[
                        'num_questions_5_in_ticket'],
                    '6': form.cleaned_data[
                        'num_problems_in_ticket'],
                    'show': form.cleaned_data['show'],
                    'output_format': form.cleaned_data['output_format'],
                    'pdf_folder': form.cleaned_data['pdf_folder']}
            num_of_tickets = get_minimal_number_of_questions(questions_pool, info,
                                                             File.objects.filter(uuid=uuid)[0].stats)
            obj = File.objects.filter(uuid=uuid)[0]
            obj.tickets = num_of_tickets
            obj.params = info
            obj.save()
            return HttpResponseRedirect(f"/exam_questions/{uuid}/num_of_tickets/{filename}")

    else:
        form = UploadParamsForm()
    return render(request, 'params.html', {'form': form})


def downloadfile(request, uuid, filename):
    if filename != '':
        if (File.objects.filter(uuid=uuid)[0].params['pdf_folder'] == False):
            path = open(f'exam_questions/static/upload/{uuid}/{filename}', 'rb')
            response = HttpResponse(path, content_type='pdf')
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
        else:
            path = open(f'exam_questions/static/upload/{uuid}/ticket_folder.zip', 'rb')
            response = HttpResponse(path, content_type="application/x-zip-compressed")
            response['Content-Disposition'] = "attachment; filename=ticket-folder"
            return response
    else:
        return HttpResponse("No such file")


def preview(request, uuid, filename):
    # if request.method == 'POST':
    return render(request, 'preview.html', {'filename': filename, 'uuid': f"upload/{uuid}/tickets.pdf"})
