from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm, UploadParamsForm
import os
import random
import mimetypes

from pdf2image import convert_from_path
from fpdf import FPDF
from PIL import Image

def handle_image(f):
    with open('exam_questions/static/upload/'+f.name, 'wb+') as destination:
        print(type(f.name))
        for chunk in f.chunks():
            destination.write(chunk)


def create_pdf(folder, name, params):
    os.chdir(folder)
    title = []
    with open(name, encoding='UTF-8') as f:
        all_questions = f.readlines()

    idx = 0
    while 'begin{document}' not in all_questions[idx]:
        title.append(all_questions[idx])
        idx += 1

    #creation
    questions_pool = {3: [], 4: [], 5: [], 6: []}
    for line in all_questions:
        if params['label_3'] in line:
            questions_pool[3].append(line)
        elif params['label_4'] in line:
            questions_pool[4].append(line)
        elif params['label_5'] in line:
            questions_pool[5].append(line)
        elif params['label_problem'] in line:
            questions_pool[6].append(line)

    with open('tickets.tex', 'w') as f:
        for line in title:
            f.write('%s\n' % line)
        f.write('\\begin{document} \n')
        for ticket in range(params['number_of_tickets']):
            f.write('\\begin{center} {\\Large Билет №%s} \\end{center} \n' % str(ticket + 1))
            questions = []
            points = [3, 4, 5, 6]
            for point in points:
                for question in range(params[point]):
                    choice = random.choice(questions_pool[point])
                    while choice in questions:
                        choice = random.choice(questions_pool[point])
                    questions.append(choice)
            f.write('\n')
            for line in questions:
                f.write('%s\n' % line)

        f.write('\\end{document}')

    os.system(f"pdflatex tickets.tex")
    os.chdir("../../..")

def create_pages(folder, name, params):
    os.chdir(folder)
    title = []
    with open(name, encoding='UTF-8') as f:
        all_questions = f.readlines()

    idx = 0
    while 'begin{document}' not in all_questions[idx]:
        if ('documentclass' in all_questions[idx]) or ('documentarticle' in all_questions[idx]) :
            idx += 1
            continue
        title.append(all_questions[idx])
        idx += 1

    #creation
    questions_pool = {3: [], 4: [], 5: [], 6:[]}
    for line in all_questions:
        if params['label_3'] in line:
            questions_pool[3].append(line)
        elif params['label_4'] in line:
            questions_pool[4].append(line)
        elif params['label_5'] in line:
            questions_pool[5].append(line)
        elif params['label_problem'] in line:
            questions_pool[6].append(line)

    for ticket in range(params['number_of_tickets']):
        questions = []
        points = [3, 4, 5, 6]
        for point in points:
            for question in range(params[point]):
                choice = random.choice(questions_pool[point])
                while choice in questions:
                    choice = random.choice(questions_pool[point])
                questions.append(choice)
        with open(f"tickets{ticket + 1}.tex", 'w') as f:
            f.write('\\documentclass[preview]{standalone} \n')
            for line in title:
                f.write('%s\n' % line)
            f.write('\\begin{document} \n')
            f.write('\\begin{center} {\\Large Билет №%s} \\end{center} \n' % str(ticket + 1))
            f.write('\n')
            for line in questions:
                f.write('%s\n' % line)
            f.write('\\end{document}')

        os.system(f"pdflatex tickets{ticket + 1}.tex")

    for ticket in range(params['number_of_tickets']):
        file = convert_from_path(f'tickets{ticket + 1}.pdf', 500)
        for fil in file:
            fil.save(f'tickets{ticket + 1}.png', 'PNG')

    pdf = FPDF()
    x_current = 20
    y_current = 20
    pdf.add_page()
    for image in [f'tickets{ticket + 1}.png' for ticket in range(params['number_of_tickets'])]:
        im = Image.open(image)
        width, height = im.size
        coef = width/160
        if (y_current + height/coef > 280):
            y_current = 20
            pdf.add_page()
        pdf.image(image, x_current, y_current, width/coef, height/coef)
        y_current += height/coef + 5
    pdf.output("tickets.pdf", "F")
    os.chdir("../../..")



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
            create_pages("exam_questions/static/upload/", filename, {'label_3': '3.png', 'label_4': '4.png',
                                                                   'label_5': '5.png', 'label_problem': 'z.png',
                                                                   'number_of_tickets': form.cleaned_data['num_tickets'],
                                                                    3: form.cleaned_data['num_questions_3_in_ticket'],
                                                                    4: form.cleaned_data['num_questions_4_in_ticket'],
                                                                    5: form.cleaned_data['num_questions_5_in_ticket'],
                                                                    6: form.cleaned_data['num_problems_in_ticket']})
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


