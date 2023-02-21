from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile

#inherit Django's registration form and adding some customizations(fname,lname,email)
class UserRegisterForm(UserCreationForm):
	fname = forms.CharField()
	lname = forms.CharField()
	email = forms.EmailField()
	class Meta:
		model = User 
		fields = ['username', 'fname', 'lname', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']