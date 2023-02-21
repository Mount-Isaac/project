from django.urls import path
from .views import (
	homepage, 
	about,
	post_details, 
	PostCreateView, 
	PostUpdateView,
	PostDeleteView,
	UserPostCreateView
	#create_post
	)

app_name = 'blog'
urlpatterns = [
	path('', homepage.as_view(), name='blog-home'),
	path('user/<str:username>', UserPostCreateView.as_view(), name='blog-userblogs'),
	path('about/', about.as_view(), name='blog-about'),
	path('posts/<int:id>/', post_details.as_view(), name = 'blog-post'),
	path('posts/<int:pk>/update/', PostUpdateView.as_view(), name = 'blog-update'),
	path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name = 'blog-delete'),
	path('post/new/', PostCreateView.as_view(), name='blog-new')
]