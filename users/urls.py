from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import register, signin, signout, profiles, ChangePassword

#app_name = 'users'
urlpatterns = [
	path('register/', register.as_view(), name='users-register'), 
	path('signin/', signin.as_view(), name='users-signin'),
	path('signout/', signout.as_view(), name='users-signout'),
	path('profile/', profiles.as_view(), name='users-profile'),
	path('password-reset/', 
		auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), 
		name='password_reset'),

	path('password-reset/done/', 
		auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
		name='password_reset_done'),

	path('password-reset-confirm/<uidb64>/<token>/', 
		auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
		name='password_reset_confirm'),


	path('password-reset-complete/', 
		auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
		name='password_reset_complete')

]