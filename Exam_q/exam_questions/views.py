from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm, UploadParamsForm
import mimetypes
from .algorithm import build_questions_from_tex
from .algorithm import doc_parsing
from .algorithm import get_statistics
from .models import File

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
        stats['num_of_q']['Задача'] = stats['num_of_q'].pop(6, "Задача")
    return render(request, 'statistics.html', {'stats': stats['table'], 'density': stats['density'], 'questions': stats['num_of_q']})

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
            filename1 = filename.split("&")[0]
            filename2 = ""
            if len(filename.split("&")) == 2:
                filename2 = filename.split("&")[1]
            _, file_extension = os.path.splitext(filename1)
            if (file_extension == '.docx'):
                tx = doc_parsing("exam_questions/static/upload/", filename1, {'label_3': '3.',
                                                                              'label_4': '4.',
                                                                              'label_5': '5.',
                                                                              'label_problem': 'Задача',
                                                                              'number_of_tickets': form.cleaned_data[
                                                                                  'num_tickets'],
                                                                              3: form.cleaned_data[
                                                                                  'num_questions_3_in_ticket'],
                                                                              4: form.cleaned_data[
                                                                                  'num_questions_4_in_ticket'],
                                                                              5: form.cleaned_data[
                                                                                  'num_questions_5_in_ticket'],
                                                                              6: form.cleaned_data[
                                                                                  'num_problems_in_ticket'],
                                                                              'show': form.cleaned_data['show'],
                                                                              'additional_file': filename2})
            elif (file_extension == '.tex'):
                tx = build_questions_from_tex("exam_questions/static/upload/", filename1, {
                    'label_3': '3.',
                    'label_4': '4.',
                    'label_5': '5.',
                    'label_problem': 'Задача',
                    'number_of_tickets': form.cleaned_data['num_tickets'],
                    3: form.cleaned_data['num_questions_3_in_ticket'],
                    4: form.cleaned_data['num_questions_4_in_ticket'],
                    5: form.cleaned_data['num_questions_5_in_ticket'],
                    6: form.cleaned_data['num_problems_in_ticket'],
                    'show': form.cleaned_data['show'],
                    'additional_file': filename2})
            else:
                return ("undefined format")
            if tx == "Error":
                return HttpResponse("Error")
            if form.cleaned_data['output_format'] == 'PDF':
                return HttpResponseRedirect(f"/exam_questions/preview/tickets.pdf")
            elif form.cleaned_data['output_format'] == 'TEX':
                return HttpResponseRedirect(f"/exam_questions/preview/tickets.tex")
            elif form.cleaned_data['output_format'] == 'DOC':
                return HttpResponseRedirect(f"/exam_questions/preview/tickets.docx")
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


