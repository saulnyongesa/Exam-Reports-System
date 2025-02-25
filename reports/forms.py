from django import forms
from .models import *
from django.forms import modelformset_factory
from django.forms.widgets import DateInput
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
        
class AdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'id_number', 'is_examination_officer']
        

class PWDChangeView(PasswordChangeView):
    form = PasswordChangeForm
    success_url = reverse_lazy('signin-url')

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentExam
        fields = ['registration_number', 'name', 'course']

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
        fields = ['course_code', 'course_name']

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = '__all__'
        
class SeriesAddForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }
        
class MarkFormAfterStudentAdd(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['exam_mark', 'cat_mark', 'project_mark']



class TrainerSignupForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = ['name', 'id_number', 'photo']
        
class TrainerUnitForm(forms.ModelForm):
    class Meta:
        model = CourseUnit
        fields = ['unit']