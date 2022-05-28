import os
import random
from pdf2image import convert_from_path
from fpdf import FPDF
from PIL import Image
import subprocess
from django.http.response import HttpResponse


def create_pages(folder, name, params):
    # os.chdir(folder)
    dir_path = os.path.dirname(folder)
    filename = os.path.join(dir_path, name)
    title = []
    with open(filename, encoding='UTF-8') as f:
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
            if not params['show']:
                if ".png" in params['label_3'] or ".jpg" in params['label_3'] or ".jpeg" in params['label_3']:
                    pos = line.find(params['label_3'])
                    line = line[pos + len(params['label_3']) + 2:]
                else:
                    line = line.replace(params['label_3'], "")
            questions_pool[3].append(line)
        elif params['label_4'] in line:
            if not params['show']:
                if ".png" in params['label_4'] or ".jpg" in params['label_4'] or ".jpeg" in params['label_4']:
                    pos = line.find(params['label_4'])
                    line = line[pos + len(params['label_4']) + 2:]
                else:
                    line = line.replace(params['label_3'], "")
            questions_pool[4].append(line)
        elif params['label_5'] in line:
            if not params['show']:
                if ".png" in params['label_5'] or ".jpg" in params['label_5'] or ".jpeg" in params['label_5']:
                    pos = line.find(params['label_5'])
                    line = line[pos + len(params['label_5']) + 2:]
                else:
                    line = line.replace(params['label_3'], "")
            questions_pool[5].append(line)
        elif params['label_problem'] in line:
            questions_pool[6].append(line)
    for ticket in range(params['number_of_tickets']):
        questions = []
        points = [3, 4, 5, 6]
        for point in points:
            for question in range(params[point]):
                try:
                    choice = random.choice(questions_pool[point])
                except:
                    return "Error"
                while choice in questions:
                    choice = random.choice(questions_pool[point])
                questions.append(choice)
        with open(os.path.join(dir_path, f"tickets{ticket + 1}.tex"), 'w') as f:
            f.write('\\documentclass[preview]{standalone} \n')
            for line in title:
                f.write('%s\n' % line)
            f.write('\\begin{document} \n')
            f.write('\\begin{center} {\\Large Билет №%s} \\end{center} \n' % str(ticket + 1))
            f.write('\n')
            for line in questions:
                f.write('%s\n' % line)
            f.write('\\end{document}')
        os.chdir(folder)
        # os.system(f"pdflatex tickets{ticket + 1}.tex")
        subprocess.run(['pdflatex', '-interaction=nonstopmode', f"tickets{ticket + 1}.tex"])
        os.chdir('../../..')


    for ticket in range(params['number_of_tickets']):
        file = convert_from_path(os.path.join(dir_path, f'tickets{ticket + 1}.pdf'), 500)
        for fil in file:
            fil.save(os.path.join(dir_path, f'tickets{ticket + 1}.png'), 'PNG')

    pdf = FPDF()
    x_current = 20
    y_current = 20
    pdf.add_page()
    for image in [os.path.join(dir_path, f'tickets{ticket + 1}.png') for ticket in range(params['number_of_tickets'])]:
        im = Image.open(image)
        width, height = im.size
        coef = width/160
        if (y_current + height/coef > 280):
            y_current = 20
            pdf.add_page()
        pdf.image(image, x_current, y_current, width/coef, height/coef)
        y_current += height/coef + 5
    pdf.output(os.path.join(dir_path, "tickets.pdf"), "F")
    # os.chdir('../../..')