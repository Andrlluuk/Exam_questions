import os
import time
import uuid

from Exam_q.celery import app
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from exam_questions.algorithm import create_pdf, create_texs, create_folder, \
    get_minimal_number_of_questions, create_questions_tex, get_statistics
from exam_questions.forms import UploadFileForm, UploadParamsForm, UploadTicketForm
from exam_questions.models import File


@app.task(queue="tasks_queue")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


"""@app.task(queue="tasks_queue")
def handle_file_task(f, uuid):
    if not os.path.exists(f'exam_questions/static/upload/{uuid}'):
        os.mkdir(f'exam_questions/static/upload/{uuid}')
    with open(f'exam_questions/static/upload/{uuid}/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@app.task(queue="tasks_queue")
def index_task(request):
    if request.method == 'POST':
        return HttpResponseRedirect(f"{uuid.uuid1()}/load")
    else:
        return render(request, 'index.html')


@app.task(queue="tasks_queue")
def statistics_task(request, uuid, filename):
    if request.method == 'POST':
        return HttpResponseRedirect(f"/exam_questions/{uuid}/params/{filename}")
    else:
        stats = File.objects.filter(uuid=uuid)[0].stats
        stats['num_of_q']['Задача'] = stats['num_of_q'].pop('6')
        return render(request, 'statistics.html',
                      {'stats': stats['table'], 'density': stats['density'], 'questions': stats['num_of_q']})


def params_for_tickets_task(request, uuid, filename):



@app.task(queue="tasks_queue")
def load_task(request, uuid):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_file_task(request.FILES['file'], uuid)
            filename = request.FILES['file']
            if (form.cleaned_data['additional_file']):
                stats, questions_pool, title = get_statistics(
                    f"exam_questions/static/upload/{uuid}/" + request.FILES['file'].name,
                    "exam_questions/static/upload/" + request.FILES['additional_file'].name)
                handle_file_task(request.FILES['additional_file'], uuid)
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

@app.task(queue="tasks_queue")
def method1(uuid, filename):




@app.task(queue="tasks_queue")
def params_task(request, uuid, filename):
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

@app.task(queue="tasks_queue")
def foo():
    return "Hello world"

@app.task(queue="tasks_queue")
def downloadfile_task(request, uuid, filename):
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


@app.task(queue="tasks_queue")
def preview_task(request, uuid, filename):
    # if request.method == 'POST':
    return render(request, 'preview.html', {'filename': filename, 'uuid': f"upload/{uuid}/tickets.pdf"})"""

