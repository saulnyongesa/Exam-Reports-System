from django import forms
from .models import *
from django.forms import modelformset_factory
from django.forms.widgets import DateInput

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentExam
        fields = ['first_name', 'second_name', 'last_name', 'registration_number', 'email', 'phone', 'course']

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['unit', 'series', 'cat_mark', 'exam_mark', 'project_mark']
        
        
MarksFormSet = modelformset_factory(Mark, form=MarkForm, extra=0)
# MarksFormSet = modelformset_factory(Mark, form=MarkForm, extra=0)  


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name', 'start_date', 'end_date', 'is_active']
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code']

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_name', 'unit_code']


class SeriesAddForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
        
        

