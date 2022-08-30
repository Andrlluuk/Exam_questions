import os
import random
from pdf2image import convert_from_path
from fpdf import FPDF
from PIL import Image
import subprocess
from docx import Document
from timeit import default_timer as timer
import re


def parse_tex(file):
    PARAMS = {'label_3': '3.',
              'label_4': '4.',
              'label_5': '5.',
              'label_problem': 'Задача'}
    title = []
    with open(file, encoding='UTF-8') as f:
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
            pos = line.find('Глава') + 5
            chapter_name = line[pos:]
            if chapter_name not in questions_pool.keys():
                questions_pool[chapter_name] = {3: {}, 4: {}, 5: {}, 6: {}}
        pos = 0
        if line.startswith(PARAMS['label_3']):
            result = re.findall('^[0-9]\.[0-9]\.', line)
            if (len(result) == 0):
                result = re.findall('^[0-9]\.', line)
            mark = result[0][0]
            frequency = 0
            if (len(result[0]) > 2):
                frequency = int(result[0][2:-1])
            question = line[len(result[0]):]
            if (frequency in questions_pool[chapter_name][3].keys()):
                questions_pool[chapter_name][3][frequency].append(question)
            else:
                questions_pool[chapter_name][3][frequency] = []
                questions_pool[chapter_name][3][frequency].append(question)
        elif line.startswith(PARAMS['label_4']):
            result = re.findall('^[0-9]\.[0-9]\.', line)
            if (len(result) == 0):
                result = re.findall('^[0-9]\.', line)
            frequency = 0
            if (len(result[0]) > 2):
                frequency = int(result[0][2:-1])
            question = line[len(result[0]):]
            if (frequency in questions_pool[chapter_name][4].keys()):
                questions_pool[chapter_name][4][frequency].append(question)
            else:
                questions_pool[chapter_name][4][frequency] = []
                questions_pool[chapter_name][4][frequency].append(question)
        elif line.startswith(PARAMS['label_5']):
            result = re.findall('^[0-9]\.[0-9]\.', line)
            if (len(result) == 0):
                result = re.findall('^[0-9]\.', line)
            frequency = 0
            if (len(result[0]) > 2):
                frequency = int(result[0][2:-1])
            question = line[len(result[0]):]
            if (frequency in questions_pool[chapter_name][5].keys()):
                questions_pool[chapter_name][5][frequency].append(question)
            else:
                questions_pool[chapter_name][5][frequency] = []
                questions_pool[chapter_name][5][frequency].append(question)
        elif line.startswith(PARAMS['label_problem']):
            result = re.findall('^Задача\.[0-9]\.', line)
            if (len(result) == 0):
                result = re.findall('^Задача\.', line)
            frequency = 0
            if (len(result[0]) > 7):
                frequency = int(result[0][8:-1])
                question = line[:len(result[0])] + line[len(result[0]) + 2:]
            question = line
            if (frequency in questions_pool[chapter_name][6].keys()):
                questions_pool[chapter_name][6][frequency].append(question)
            else:
                questions_pool[chapter_name][6][frequency] = []
                questions_pool[chapter_name][6][frequency].append(question)

    return questions_pool, title

def parse_docx(file):
    PARAMS = {'label_3': '3.',
              'label_4': '4.',
              'label_5': '5.',
              'label_problem': 'Задача'}
    title = []
    questions_pool = {}
    doc = Document(file)
    chapter_name = 1
    for line in doc.paragraphs:
        line = line.text
        if len(line) == 0:
            continue
        if line[0] == '%':
            continue
        if 'Глава' in line:
            pos = line.find('Глава') + 5
            chapter_name = line[pos:]
        if chapter_name not in questions_pool.keys():
            questions_pool[chapter_name] = {3: {}, 4: {}, 5: {}, 6: {}}
        pos = 0
        if line.startswith(PARAMS['label_3']):
            result = re.findall('^[0-9]\.[0-9]\.', line)
            if (len(result) == 0):
                result = re.findall('^[0-9]\.', line)
            mark = result[0][0]
            frequency = 0
            if (len(result[0]) > 2):
                frequency = int(result[0][2:-1])
            question = line[len(result[0]):]
            if (frequency in questions_pool[chapter_name][3].keys()):
                questions_pool[chapter_name][3][frequency].append(question)
            else:
                questions_pool[chapter_name][3][frequency] = []
                questions_pool[chapter_name][3][frequency].append(question)
        elif line.startswith(PARAMS['label_4']):
            result = re.findall('^[0-9]\.[0-9]\.', line)
            if (len(result) == 0):
                result = re.findall('^[0-9]\.', line)
            frequency = 0
            if (len(result[0]) > 2):
                frequency = int(result[0][2:-1])
            question = line[len(result[0]):]
            if (frequency in questions_pool[chapter_name][4].keys()):
                questions_pool[chapter_name][4][frequency].append(question)
            else:
                questions_pool[chapter_name][4][frequency] = []
                questions_pool[chapter_name][4][frequency].append(question)
        elif line.startswith(PARAMS['label_5']):
            result = re.findall('^[0-9]\.[0-9]\.', line)
            if (len(result) == 0):
                result = re.findall('^[0-9]\.', line)
            frequency = 0
            if (len(result[0]) > 2):
                frequency = int(result[0][2:-1])
            question = line[len(result[0]):]
            if (frequency in questions_pool[chapter_name][5].keys()):
                questions_pool[chapter_name][5][frequency].append(question)
            else:
                questions_pool[chapter_name][5][frequency] = []
                questions_pool[chapter_name][5][frequency].append(question)
        elif line.startswith(PARAMS['label_problem']):
            result = re.findall('^Задача\.[0-9]\.', line)
            if (len(result) == 0):
                result = re.findall('^Задача\..', line)
            frequency = 0
            if (len(result[0]) > 5):
                frequency = int(result[0][8:-1])
                question = line[:len(result[0])] + line[len(result[0]) + 2:]
            question = line
            if (frequency in questions_pool[chapter_name][6].keys()):
                questions_pool[chapter_name][6][frequency].append(question)
            else:
                questions_pool[chapter_name][6][frequency] = []
                questions_pool[chapter_name][6][frequency].append(question)

    return questions_pool, title

def parse_txt(*params):
    """TODO"""