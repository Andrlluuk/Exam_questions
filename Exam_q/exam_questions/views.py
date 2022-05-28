from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm, UploadParamsForm
import mimetypes
from .algorithm import create_pages

def handle_image(f):
    with open('exam_questions/static/upload/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    return render(request, 'index.html')

def load(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_image(request.FILES['file'])
            return HttpResponseRedirect(f"/exam_questions/{request.FILES['file'].name}")
    else:
        form = UploadFileForm()
    return render(request, 'load.html', {'form': form})

def params(request, filename):
    if request.method == 'POST':
        form = UploadParamsForm(request.POST, request.FILES)
        if form.is_valid():
            if(form.cleaned_data['label_3']):
                handle_image(request.FILES['label_3'])
            if (form.cleaned_data['label_4']):
                handle_image(request.FILES['label_4'])
            if (form.cleaned_data['label_5']):
                handle_image(request.FILES['label_5'])
            if (form.cleaned_data['label_problem']):
                handle_image(request.FILES['label_problem'])

            create_pages("exam_questions/static/upload/", filename, {'label_3': str(request.FILES['label_3']) if form.cleaned_data['label_3'] else 'Вопрос на 3.',
                                                                     'label_4': str(request.FILES['label_4']) if form.cleaned_data['label_4'] else 'Вопрос на 4.',
                                                                     'label_5': str(request.FILES['label_5']) if form.cleaned_data['label_5'] else 'Вопрос на 5.',
                                                                     'label_problem': str(request.FILES['label_problem']) if form.cleaned_data['label_problem'] else 'Задача',
                                                                   'number_of_tickets': form.cleaned_data['num_tickets'],
                                                                    3: form.cleaned_data['num_questions_3_in_ticket'],
                                                                    4: form.cleaned_data['num_questions_4_in_ticket'],
                                                                    5: form.cleaned_data['num_questions_5_in_ticket'],
                                                                    6: form.cleaned_data['num_problems_in_ticket'],
                                                                    'show': form.cleaned_data['show']})

            if form.cleaned_data['output_format'] == 'PDF':
                return HttpResponseRedirect(f"/exam_questions/preview/tickets.pdf")
            elif form.cleaned_data['output_format'] == 'TEX':
                return HttpResponseRedirect(f"/exam_questions/preview/tickets.tex")
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


