from django import forms
from .models import Task
 
# creating a form

class DateInput(forms.DateInput):
    input_type = 'date'


class Create_Form(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'complete', 'date']
        widgets = {'date' : DateInput()}

