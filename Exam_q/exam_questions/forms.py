from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Программа')

class UploadParamsForm(forms.Form):
    num_tickets = forms.IntegerField(label='Количество билетов')
    CHOICES = (
        ('PDF', '.pdf'),
        ('TEX', '.tex'),
    )
    label_3 = forms.FileField(required=False, label='Лейбл для вопросов на 3')
    num_questions_3_in_ticket = forms.IntegerField(label='Количество вопросов на 3 в билете')
    label_4 = forms.FileField(required=False, label='Лейбл для вопросов на 4')
    num_questions_4_in_ticket = forms.IntegerField(label='Количество вопросов на 4 в билете')
    label_5 = forms.FileField(required=False, label='Лейбл для вопросов на 5')
    num_questions_5_in_ticket = forms.IntegerField(label='Количество вопросов на 5 в билете')
    label_problem = forms.FileField(required=False, label='Лейбл для задач')
    num_problems_in_ticket = forms.IntegerField(label='Количество задач в билете')
    output_format = forms.ChoiceField(choices=CHOICES, label='Выходной формат файла')