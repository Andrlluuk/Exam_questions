from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm


def index(request):
    # Imaginary function to handle an uploaded file.
    # from somewhere import handle_uploaded_file

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'index.html', {'form': form})