from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileUpdateForm, UserUpdateForm

# Create your views here.
class register(View):
	templates_name = 'users/register.html'

	def get(self, request, *args, **kwargs):
		form = UserRegisterForm()
		context = {
			"form": form 
		}

		return render(request, self.templates_name, context)

	def post(self, request, *args, **kwargs):
		# get posted user data
		form = UserRegisterForm(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			fname = form.cleaned_data.get('fname')
			lname = form.cleaned_data.get('lname')
			email = form.cleaned_data.get('email')
			password1 = form.cleaned_data.get('password1')
			password2 = form.cleaned_data.get('password2')

			if password1 != password2:
				messages.error(request, "Password mismatch")
				return redirect('users-register')

			if User.objects.filter(username=username).exists():
				messages.error(request, "Username exists")
				return redirect('users-register')

			if User.objects.filter(email=email).exists():
				messages.error(request, "Email exists!")
				return redirect('users-register')

			my_user = User.objects.create_user(username, email, password1)
			my_user.first_name = fname
			my_user.last_name = lname
			my_user.save()

			messages.success(request, "Account created successfully")
			return redirect('users-signin')
		else:
			return render(request, self.templates_name, {"form": form})



class signin(View):
	templates_name = "users/login.html"

	def get(self, request, *args, **kwargs):
		context = {
			"form": AuthenticationForm()
		}
		return render(request, self.templates_name, context)

	def post(self, request, *args, **kwargs):
		username = request.POST.get('username')
		password1 = request.POST.get('password')

		user = authenticate(username=username, password=password1)
		if user is not None:
			login(request, user)
			return redirect("blog:blog-home")
		else:
			messages.error(request, "Invalid credentials")
			return redirect("users-signin")

class signout(View):
	templates_name = "users/signout.html"

	def get(self, request):
		logout(request)
		return render(request, self.templates_name)



class ChangePassword(LoginRequiredMixin, View):
	templates_name = 'users/change_password.html'

	def get(self, request, *args, **kwargs):
		form = PasswordChangeForm(request.user)
		context = {
			"form":form
		}

		return render(request, self.templates_name, context)






#requires login in order to be accessed 
class profiles(LoginRequiredMixin, View):
	templates_name = 'users/profile.html'

	def get(self, request, *args, **kwargs):
		u_form = UserUpdateForm()
		p_form = ProfileUpdateForm()
		context = {
			"u_form": u_form, 
			"p_form": p_form
		}

		return render(request, self.templates_name, context)

	def post(self, request, *args, **kwargs):
		u_form = UserUpdateForm(request.POST or None, instance=request.user)
		p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance=request.user.profile)

		try:
			if u_form.is_valid() and p_form.is_valid():
				u_form.save()
				p_form.save()

				messages.success(request, 'Your account has been updated')
				return redirect("users-profile")
		
		except Exception as e:
			messages.error(request, str(e))
			return redirect("users-profile")