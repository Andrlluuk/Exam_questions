import math

def collect_statistics(question_pool, additional_questions_pool = None):
    stats = {}
    table = {}
    quest_density = {}
    for key in question_pool.keys():
        for mark in question_pool[key].keys():
            quest_density[mark] = 0
    idx = 0
    for key in question_pool.keys():
        idx += 1
        new_key = f"Глава {idx}"
        table[new_key] = []
        for mark in question_pool[key].keys():
            result = ""
            for difficulty in range(1, 6):
                if difficulty in question_pool[key][mark].keys():
                    quest_density[mark] += len(question_pool[key][mark][difficulty])/difficulty
                    result += f"Частоты {str(difficulty)} - {str(len(question_pool[key][mark][difficulty]))}\n"
            if result != "":
                table[new_key].append(result)
            else:
                table[new_key].append("Нет обязательных вопросов")
            if 0 in question_pool[key][mark].keys():
                table[new_key].append(len(question_pool[key][mark][0]))
            else:
                table[new_key].append(0)
            round(quest_density[mark], 3)

    if (additional_questions_pool != None):
        for key in additional_questions_pool.keys():
            for mark in additional_questions_pool[key].keys():
                if mark not in quest_density.keys():
                    quest_density[mark] = 0
        idx = 0
        for key in additional_questions_pool.keys():
            idx += 1
            new_key = f"Глава {idx}"
            table[new_key] = []
            for mark in additional_questions_pool[key].keys():
                result = ""
                for difficulty in range(1, 6):
                    if difficulty in additional_questions_pool[key][mark].keys():
                        quest_density[mark] += len(additional_questions_pool[key][mark][difficulty]) / difficulty
                        result += f"Частоты {str(difficulty)} - {str(len(additional_questions_pool[key][mark][difficulty]))}\n"
                if result != "":
                    table[new_key].append(result)
                else:
                    table[new_key].append("Нет обязательных вопросов")
                if 0 in additional_questions_pool[key][mark].keys():
                    table[new_key].append(len(additional_questions_pool[key][mark][0]))
                else:
                    table[new_key].append(0)
                round(quest_density[mark], 3)

    stats['table'] = table
    stats['density'] = quest_density
    least_number_of_questions = {}
    for key in quest_density.keys():
        least_number_of_questions[key] = math.ceil(quest_density[key])
    stats['num_of_q'] = least_number_of_questions


    return stats





