from django import forms
from django.core.validators import MinValueValidator


class UploadFileForm(forms.Form):
    file = forms.FileField(label='Программа')
    additional_file = forms.FileField(required=False, label='Дополнительный файл')


class UploadNextForm(forms.Form):
    pass


class UploadTicketForm(forms.Form):
    num_problems_in_ticket = forms.IntegerField(label='Количество билетов')


class UploadParamsForm(forms.Form):
    CHOICES = (
        ('PDF', '.pdf'),
        ('TEX', '.tex'),
        ('DOC', '.doc')
    )
    show = forms.BooleanField(required=False, label='Показывать сложность вопросов в билетах')
    num_questions_3_in_ticket = forms.IntegerField(validators=[
    MinValueValidator(0,message="Поле для вопросов на оценку 3 должно быть больше 0")],
                                               label='Количество вопросов на 3 в билете')
    num_questions_4_in_ticket = forms.IntegerField(validators=[
    MinValueValidator(0,message="Поле для вопросов на оценку 4 должно быть больше 0")],
                                               label='Количество вопросов на 4 в билете')
    num_questions_5_in_ticket = forms.IntegerField(validators=[
    MinValueValidator(0,message=f"Поле для вопросов на оценку 5 должно быть больше 0")],
                                               label='Количество вопросов на 5 в билете')
    num_problems_in_ticket = forms.IntegerField(
    validators=[MinValueValidator(0, message=f"Поле для задач должно быть больше 0")],
    label='Количество задач в билете')
    output_format = forms.ChoiceField(choices=CHOICES, label='Выходной формат файла')
    #pdf_folder = forms.BooleanField(required=False, label='Сделать каждый билет отдельным pdf-файлом')
