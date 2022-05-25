from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Программа')

class UploadParamsForm(forms.Form):
    num_tickets = forms.IntegerField(label='Количество билетов')
    CHOICES = (
        ('PDF', '.pdf'),
        ('TEX', '.tex'),
    )
    num_questions_3_in_ticket = forms.IntegerField(label='Количество вопросов на 3')
    num_questions_4_in_ticket = forms.IntegerField(label='Количество вопросов на 4')
    num_questions_5_in_ticket = forms.IntegerField(label='Количество вопросов на 5')
    output_format = forms.ChoiceField(choices=CHOICES, label='Выходной формат файла')