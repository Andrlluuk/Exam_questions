from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm, UploadParamsForm, UploadTicketForm
import mimetypes
from .algorithm import build_questions_from_tex
from .algorithm import doc_parsing, create_pdf, create_texs
from .algorithm import get_statistics
from .models import File
from .algorithm import get_minimal_number_of_questions, create_questions_tex

import os


def handle_file(f):
    with open('exam_questions/static/upload/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    return render(request, 'index.html')

def statistics(request, filename):
    if request.method == 'POST':
        return HttpResponseRedirect(f"/exam_questions/params/{filename}")
    else:
        stats = File.objects.filter(filename=filename)[0].stats
        stats['num_of_q']['Задача'] = stats['num_of_q'].pop('6')
    return render(request, 'statistics.html', {'stats': stats['table'], 'density': stats['density'], 'questions': stats['num_of_q']})

def params_for_tickets(request, filename):
    """TODO(docx)"""
    if request.method == 'POST':
        form = UploadTicketForm(request.POST, request.FILES)
        if form.is_valid():
            obj = File.objects.filter(filename=filename)[0]
            obj.tickets = form.cleaned_data['num_problems_in_ticket']
            obj.save()
            obj = File.objects.filter(filename=filename)[0]
            filename = obj.filename

            _, file_extension = os.path.splitext(filename)
            if (file_extension == '.docx'):
                tx = doc_parsing("exam_questions/static/upload/", filename, {
                    'label_3': str(request.FILES['label_3']) if form.cleaned_data['label_3'] else 'Вопрос на 3',
                    'label_4': str(request.FILES['label_4']) if form.cleaned_data['label_4'] else 'Вопрос на 4',
                    'label_5': str(request.FILES['label_5']) if form.cleaned_data['label_5'] else 'Вопрос на 5',
                    'label_problem': str(request.FILES['label_problem']) if form.cleaned_data[
                        'label_problem'] else 'Задача',
                    'number_of_tickets': form.cleaned_data['num_tickets'],
                    3: form.cleaned_data['num_questions_3_in_ticket'],
                    4: form.cleaned_data['num_questions_4_in_ticket'],
                    5: form.cleaned_data['num_questions_5_in_ticket'],
                    6: form.cleaned_data['num_problems_in_ticket'],
                    'show': form.cleaned_data['show']})
            else:
                questions = create_questions_tex("exam_questions/static/upload/", filename, obj.params,
                                                 obj.questions_pool, obj.tickets)
                create_texs(questions, obj.params, "exam_questions/static/upload/", "exam_questions/static/upload/")
                create_pdf(questions, obj.params, obj.tickets, "exam_questions/static/upload/", "exam_questions/static/upload/")
            if questions == "Error":
                return HttpResponse("Error")
            if obj.output_format == 'PDF':
                return HttpResponseRedirect(f"/exam_questions/preview/tickets.pdf")
            elif obj.output_format == 'TEX':
                return HttpResponseRedirect(f"/exam_questions/preview/tickets.tex")
    else:
        form = UploadTicketForm()
        num = File.objects.filter(filename=filename)[0].tickets
        return render(request, 'ticket_suggestion.html', {'form': form, 'num_of_tickets': num})


def load(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_file(request.FILES['file'])
            filename = request.FILES['file']
            if(form.cleaned_data['additional_file']):
                stats, questions_pool, title = get_statistics("exam_questions/static/upload/" + request.FILES['file'].name,
                               "exam_questions/static/upload/" + request.FILES['additional_file'].name)
                handle_file(request.FILES['additional_file'])
                if (len(File.objects.filter(filename=filename)) != 0 ):
                    File.objects.filter(filename=filename)[0].delete()
                File(filename=filename, questions_pool=questions_pool, stats=stats, title=title).save()
                return HttpResponseRedirect(f"/exam_questions/statistics/{filename}")
            else:
                stats, questions_pool, title = get_statistics("exam_questions/static/upload/" + request.FILES['file'].name)
                if (len(File.objects.filter(filename=filename)) != 0 ):
                    File.objects.filter(filename=filename)[0].delete()
                File(filename=filename, questions_pool=questions_pool, stats=stats, title=title).save()
                return HttpResponseRedirect(f"/exam_questions/statistics/{filename}")
    else:
        form = UploadFileForm()
    return render(request, 'load.html', {'form': form})

def params(request, filename):
    if request.method == 'POST':
        form = UploadParamsForm(request.POST, request.FILES)
        if form.is_valid():
            questions_pool = File.objects.filter(filename=filename)[0].questions_pool
            info = {'3': form.cleaned_data['num_questions_3_in_ticket'],
                                                              '4': form.cleaned_data[
                                                                  'num_questions_4_in_ticket'],
                                                              '5': form.cleaned_data[
                                                                  'num_questions_5_in_ticket'],
                                                              '6': form.cleaned_data[
                                                                  'num_problems_in_ticket'],
                                                              'show': form.cleaned_data['show'],
                                                              'output_format': form.cleaned_data['output_format']}
            num_of_tickets = get_minimal_number_of_questions(questions_pool, info,
                                                             File.objects.filter(filename=filename)[0].stats)
            obj = File.objects.filter(filename=filename)[0]
            obj.tickets = num_of_tickets
            obj.params = info
            obj.save()
            return HttpResponseRedirect(f"/exam_questions/num_of_tickets/{filename}")

    else:
        form = UploadParamsForm()
    return render(request, 'params.html', {'form': form})

def downloadfile(request, filename):
    if filename != '':
        path = open(f'exam_questions/static/upload/{filename}', 'rb')
        mime_type, _ = mimetypes.guess_type(f'/exam_questions/static/upload/{filename}')
        response = HttpResponse(path, content_type='pdf')
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        return response
    else:
        return HttpResponse("No such file")

def preview(request, filename):
    # if request.method == 'POST':
    return render(request, 'preview.html', {'filename': filename})


