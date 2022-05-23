from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm, UploadParamsForm
from django.urls import path

def handle_image(f):
    with open('exam_questions/static/upload/'+f.name, 'wb+') as destination:
        print(type(f.name))
        for chunk in f.chunks():
            destination.write(chunk)


def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_image(request.FILES['file'])
            return HttpResponseRedirect(f"/exam_questions/{request.FILES['file'].name}")
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})

def params(request, filename):
    if request.method == 'POST':
        form = UploadParamsForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect(f"/exam_questions/{filename}/success")
    else:
        form = UploadParamsForm()
    return render(request, 'params.html', {'form': form})