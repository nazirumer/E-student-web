from django.forms import forms,ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','password1','password2']
		exclude =['email']
class CustomerForm(ModelForm):
	class Meta:
		model = Student
		fields="__all__"
		exclude=['user','enroll_year','section','position']


class TeacherForm(ModelForm):
	class Meta:
		model = Teacher
		fields="__all__"
		exclude=['user','department']

class ArrangementForm(ModelForm):
	class Meta:
		model = TeacherArrangment
		fields="__all__"
class SemisterForm(ModelForm):
	class Meta:
		model=Semister
		fields="__all__"
