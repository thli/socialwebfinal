from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse
from vinterest.models import *
from vinterest.forms import *
from django import forms

# Create your views here.
def index(request):
	context = {}
	
	if(request.method == 'GET'):
		posts = Post.objects.all()
		context['posts'] = posts
		return render(request, 'index.html', context)
		
	if(request.method == 'POST'):
		if not 'url' in request.POST or not request.POST['url']:
			return redirect(reverse('index'))
		else:
			post = Post.objects.create_post(request.user, request.POST['url'])
			post.save()
			return redirect(reverse('index'))
		
def login_user(request):
	context = {}
	if(request.user.is_authenticated()):
		return redirect(reverse('index'))
		
	else:
		l_form = LoginForm(auto_id=False)
		r_form = RegistrationForm(auto_id=False)
		context['l_form'] = l_form
		context['r_form'] = r_form
		return render(request, 'login.html', context)

def auth(request):
	context = {}
	if(request.method == 'GET'):
		return redirect(reverse('login'))
	
	if(request.method == 'POST'):
		l_form = LoginForm(request.POST)
		if not l_form.is_valid():
			context['l_form'] = l_form
			context['r_form'] = RegistrationForm(auto_id=False)
			return redirect(reverse('login'))
		
		user = authenticate(username = l_form.cleaned_data['l_username'], password = l_form.cleaned_data['l_password'])
		if user is not None:
			login(request, user)
			return redirect(reverse('index'))
		else:
			context['l_form'] = l_form
			context['r_form'] = RegistrationForm(auto_id=False)
			return render(request, 'login.html', context)
			
def register(request):
	context = {}
	if(request.method == 'GET'):
		return redirect(reverse('login'))
		
	if(request.method == 'POST'):
		r_form = RegistrationForm(request.POST)
		if not r_form.is_valid():
			context['r_form'] = r_form
			context['l_form'] = LoginForm(auto_id=False)
			return redirect(reverse('login'))
						
    # Creates the new user from the valid form data
		new_user = User.objects.create_user(username=r_form.cleaned_data['r_username'],
																				email=r_form.cleaned_data['r_email'],
                                        password=r_form.cleaned_data['r_password1'])
																				
		new_user.save()
		new_user = authenticate(username=request.POST['r_username'], \
                            password=request.POST['r_password1'])
		login(request, new_user)
		return redirect(reverse('index'))
		
def logout_user(request):
	logout(request)
	return redirect(reverse('login'))
		
		
		
		
		