import os
import random
from pdf2image import convert_from_path
from fpdf import FPDF
from PIL import Image
import subprocess
from docx import Document
from timeit import default_timer as timer

meta_info = {}

def remove_newline_signs(line):
    while (line.endswith('\n')) or (line.endswith('\\')) or (line.endswith('  ')):
        line = line[:-2]
    return line

def parse_doc(folder, name, params):
    dir_path = os.path.dirname(folder)
    filename = os.path.join(dir_path, name)
    doc = Document(filename)
    all_questions = []
    questions_pool = {}
    part_number = 0
    questions_pool[part_number] = {3: [], 4: [], 5: [], 6: []}
    for line in doc.paragraphs:
        line = line.text
        if len(line) == 0:
            continue
        if line[0] == '%':
            continue
        if 'Глава' in line:
            part_number += 1
            questions_pool[part_number] = {3: [], 4: [], 5: [], 6: []}
        if line.startswith(params['label_3']):
            if not params['show']:
                if ".png" in params['label_3'] or ".jpg" in params['label_3'] or ".jpeg" in params['label_3']:
                    pos = line.find(params['label_3'])
                    line = line[pos + len(params['label_3']) + 2:]
                else:
                    line = line.replace(params['label_3'], "")
                for i, x in enumerate(line):
                    if x.isalpha():  # True if its a letter
                        po = i  # first letter position
                        break

                line = line[po:]
            questions_pool[part_number][3].append(line)
        elif line.startswith(params['label_4']):
            if not params['show']:
                if ".png" in params['label_4'] or ".jpg" in params['label_4'] or ".jpeg" in params['label_4']:
                    pos = line.find(params['label_4'])
                    line = line[pos + len(params['label_4']) + 2:]
                else:
                    line = line.replace(params['label_4'], "")
                for i, x in enumerate(line):
                    if x.isalpha():  # True if its a letter
                        po = i  # first letter position
                        break

                line = line[po:]
            questions_pool[part_number][4].append(line)
        elif line.startswith(params['label_5']):
            if not params['show']:
                if ".png" in params['label_5'] or ".jpg" in params['label_5'] or ".jpeg" in params['label_5']:
                    pos = line.find(params['label_5'])
                    line = line[pos + len(params['label_5']) + 2:]
                else:
                    line = line.replace(params['label_5'], "")
                for i, x in enumerate(line):
                    if x.isalpha():  # True if its a letter
                        po = i  # first letter position
                        break

                line = line[po:]
            questions_pool[part_number][5].append(line)
        elif line.startswith(params['label_problem']):
            questions_pool[part_number][6].append(line)

    return questions_pool, dir_path

def parse_tex(folder, name, params):
    # os.chdir(folder)
    dir_path = os.path.dirname(folder)
    filename = os.path.join(dir_path, name)
    title = []
    with open(filename, encoding='UTF-8') as f:
        all_questions = f.readlines()
    idx = 0
    while 'begin{document}' not in all_questions[idx]:
        if ('documentclass' in all_questions[idx]) or ('documentarticle' in all_questions[idx]):
            idx += 1
            continue
        title.append(all_questions[idx])
        idx += 1

    po = 0
    # creation
    questions_pool = {}
    part_number = 0
    for line in all_questions:
        if len(line) == 0:
            continue
        if line[0] == '%':
            continue
        if 'Глава' in line:
            part_number += 1
            questions_pool[part_number] = {3: [], 4: [], 5: [], 6: []}
        if line.startswith(params['label_3']):
            if not params['show']:
                if ".png" in params['label_3'] or ".jpg" in params['label_3'] or ".jpeg" in params['label_3']:
                    pos = line.find(params['label_3'])
                    line = line[pos + len(params['label_3']) + 2:]
                else:
                    line = line.replace(params['label_3'], "")
                for i, x in enumerate(line):
                    if x.isalpha():  # True if its a letter
                        po = i  # first letter position
                        break

                line = line[po:]
            questions_pool[part_number][3].append(line)
        elif line.startswith(params['label_4']):
            if not params['show']:
                if ".png" in params['label_4'] or ".jpg" in params['label_4'] or ".jpeg" in params['label_4']:
                    pos = line.find(params['label_4'])
                    line = line[pos + len(params['label_4']) + 2:]
                else:
                    line = line.replace(params['label_4'], "")
                for i, x in enumerate(line):
                    if x.isalpha():  # True if its a letter
                        po = i  # first letter position
                        break

                line = line[po:]
            questions_pool[part_number][4].append(line)
        elif line.startswith(params['label_5']):
            if not params['show']:
                if ".png" in params['label_5'] or ".jpg" in params['label_5'] or ".jpeg" in params['label_5']:
                    pos = line.find(params['label_5'])
                    line = line[pos + len(params['label_5']) + 2:]
                else:
                    line = line.replace(params['label_5'], "")
                for i, x in enumerate(line):
                    if x.isalpha():  # True if its a letter
                        po = i  # first letter position
                        break

                line = line[po:]
            questions_pool[part_number][5].append(line)
        elif line.startswith(params['label_problem']):
            questions_pool[part_number][6].append(line)

    return questions_pool, dir_path, title


def create_texs(questions_pool, params, dir_path, folder, title = []):
    keys = []
    for key in questions_pool.keys():
        keys.append(key)
    num_of_q = params[3] + params[4] + params[5] + params[6]
    num_of_topics = len(keys)
    if num_of_topics != 0:
        density = num_of_q/num_of_topics
    else:
        density = num_of_q
    for ticket in range(params['number_of_tickets']):
        weights = {}
        for key in questions_pool.keys():
            weights[key] = 0
        questions = []
        points = [3, 4, 5, 6]
        for point in points:
            for question in range(params[point]):
                try:
                    part_choice = random.choice(keys)
                    start = timer()
                    while len(questions_pool[part_choice][point]) == 0:
                        part_choice = random.choice(keys)
                        if timer() - start > 1:
                            return "Error"
                    choice = random.choice(questions_pool[part_choice][point])
                except:
                    return "Error"
                start = timer()
                while (choice in questions) or (weights[part_choice] >= density):
                    part_choice = random.choice(keys)
                    while len(questions_pool[part_choice][point]) == 0:
                        part_choice = random.choice(keys)
                    choice = random.choice(questions_pool[part_choice][point])
                    if timer() - start > 1:
                        return "Error"
                questions.append(choice)
                weights[part_choice] += 1
        with open(os.path.join(dir_path, f"tickets{ticket + 1}.tex"), 'w') as f:
            f.write('\\documentclass[preview]{standalone} \n')
            if title != []:
                for line in title:
                    f.write('%s\n' % line)
            else:
                f.write('\\usepackage[english, russian]{babel} \n')
            f.write('\\begin{document} \n')
            f.write('\\begin{center} {\\Large Билет №%s} \\end{center} \n' % str(ticket + 1))
            f.write('\n')
            for i in range(len(questions)):
                line = remove_newline_signs(questions[i])
                if not params['show']:
                    f.write('%s' % f'{i + 1}. ' + line)
                else:
                    f.write('%s' % line)
                f.write('\\\\\n')
                f.write('\n')
            f.write('\\end{document}')
        os.chdir(folder)
        # os.system(f"pdflatex tickets{ticket + 1}.tex")
        subprocess.run(['pdflatex', '-interaction=nonstopmode', f"tickets{ticket + 1}.tex"])
        os.chdir('../../..')

def create_pdf(questions_pool, params, dir_path, folder, title = []):
    for ticket in range(params['number_of_tickets']):
        file = convert_from_path(os.path.join(dir_path, f'tickets{ticket + 1}.pdf'), 500)
        for fil in file:
            fil.save(os.path.join(dir_path, f'tickets{ticket + 1}.png'), 'PNG')

    pdf = FPDF()
    x_current = 20
    y_current = 5
    max_height = 0
    for image in [os.path.join(dir_path, f'tickets{ticket + 1}.png') for ticket in range(params['number_of_tickets'])]:
        im = Image.open(image)
        width, height = im.size
        coef = width / 160
        max_height = max(height / coef, max_height)
    pdf.add_page()
    for image in [os.path.join(dir_path, f'tickets{ticket + 1}.png') for ticket in range(params['number_of_tickets'])]:
        im = Image.open(image)
        width, height = im.size
        coef = width / 160
        if y_current + max_height > 292:
            y_current = 5
            pdf.add_page()
        y_current += 5
        pdf.image(image, x_current, y_current, width / coef, height / coef)
        y_current += max_height + 5
        pdf.line(0, y_current, 297, y_current)
    pdf.output(os.path.join(dir_path, "tickets.pdf"), "F")
    # os.chdir('../../..')

def create_pages(folder, name, params):
    questions_pool, dir_path, title = parse_tex(folder, name, params)
    if (params['additional_file']):
        _, file_extension = os.path.splitext(params['additional_file'])
        if file_extension == ".tex":
            questions_pool_additional, _, _ = parse_tex(folder, params['additional_file'], params)
        elif file_extension == ".doc" or file_extension == ".docx":
            questions_pool_additional, _ = parse_doc(folder, params['additional_file'], params)
        for i in range(1, min(len(questions_pool), len(questions_pool_additional))):
            for key in questions_pool[i].keys():
                questions_pool[i][key].extend(questions_pool_additional[i][key])
    if create_texs(questions_pool, params, dir_path, folder, title) == "Error":
        return "Error"
    create_pdf(questions_pool, params, dir_path, folder, title)

def doc_parsing(folder, name, params):
    questions_pool, dir_path = parse_doc(folder, name, params)
    if (params['additional_file']):
        _, file_extension = os.path.splitext(params['additional_file'])
        if file_extension == ".tex":
            questions_pool_additional, _, _ = parse_tex(folder, params['additional_file'], params)
        elif file_extension == ".doc" or file_extension == ".docx":
            questions_pool_additional, _ = parse_doc(folder, params['additional_file'], params)
        for i in range(1, min(len(questions_pool), len(questions_pool_additional))):
            for key in questions_pool[i].keys():
                questions_pool[i][key].extend(questions_pool_additional[i][key])
    if create_texs(questions_pool, params, dir_path, folder) == "Error":
        return "Error"
    create_pdf(questions_pool, params, dir_path, folder)