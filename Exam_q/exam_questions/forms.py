from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class UploadParamsForm(forms.Form):
    num_tickets = forms.IntegerField()
    CHOICES = (
        ('PDF', '.pdf'),
        ('TEX', '.tex'),
    )
    num_questions_3_in_ticket = forms.IntegerField()
    num_questions_4_in_ticket = forms.IntegerField()
    num_questions_5_in_ticket = forms.IntegerField()
    output_format = forms.ChoiceField(choices=CHOICES)