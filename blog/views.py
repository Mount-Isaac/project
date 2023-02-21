from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.models import User
from .forms import CreateNewPost
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

class homepage(View):
	template_name = 'blog/index.html'

	def get(self, request, *args, **kwargs):
		posts_list = Post.objects.all().order_by('-date_posted') # select *from table_name order by DESC

		page = request.GET.get('page', 1)
		paginator = Paginator(posts_list, 4)

		try:
			posts = paginator.page(page)
		except PageNotAnInteger: 
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.num_pages()


		context = {
			"posts" : posts
		}
		
		#post = Post.objects.get(pk=1)
		#print('POST Details: ', dir(post.author))
		return render(request, self.template_name, context)


class UserPostCreateView(ListView):
	template_name = 'blog/users_posts.html'

	def get(self, request, *args, **kwargs):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		posts_list = Post.objects.filter(author=user).order_by('-date_posted') # select *from table_name order by DESC

		page = request.GET.get('page', 1)
		paginator = Paginator(posts_list, 4)

		try:
			posts = paginator.page(page)
		except PageNotAnInteger: 
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.num_pages()

		context = {
			"posts" : posts,
			"username": self.kwargs.get('username'),
			"user_total_pages": posts_list.count()
		}
		#print("username here: ",context.get('username'))
		#print('user_total_pages: ',context.get('user_total_pages') )
		#post = Post.objects.get(pk=1)
		#print('POST Details: ', dir(post.author))
		return render(request, self.template_name, context)



class error_404(View):
	template_name = '404.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name)



class about(View):
	template_name = 'blog/about.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {})


class post_details(View):
	template_name = 'blog/posts.html'

	def get(self, request, id=id, *args, **kwargs):
		obj = Post.objects.get(pk=id)
		context = {"post":obj}
		return render(request, self.template_name, context)

# class create_post(View):
# 	template_name = 'blog/post_create.html'

# 	def get(self, request, *args, **kwargs):
# 		form = CreateNewPost()
# 		context = {"form":form}
# 		return render(request, self.template_name, context)


# 	def post(self, request, *args, **kwargs):
# 		form = CreateNewPost(request.POST or None, form.instance.author = Post.author)

# 		if form.is_valid():
# 			form.save()
# 			return redirect('blog:blog-home')

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post  
	fields = ['title', 'content']


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post  
	fields = ['title', 'content']


	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

	model = Post
	success_url  = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


