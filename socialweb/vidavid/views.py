from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.urlresolvers import reverse

from vidavid.models import *
from vidavid.forms import *
from django import forms

# Create your views here.
#-------------------------------------------------------------#
#                     User authentication                     #
#-------------------------------------------------------------#
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
            messages.success(request, 'Login successful!')   
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Form was incorrectly filled out')
            return redirect(reverse('login'))

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
        messages.success(request, 'Registration successful!')
        return redirect(reverse('index'))

@login_required(login_url="/vidavid/login")       
def logout_user(request):
    logout(request)
    return redirect(reverse('login'))

    
    
#-------------------------------------------------------------#
#                           Content                           #
#-------------------------------------------------------------#
    
def index(request):
    context = {}
    posts = Post.objects.all().order_by('-id')
    context['posts'] = posts	
    context['post_form'] = PostForm()
    context['user'] = request.user
    if(request.method == 'GET'):
        return render(request, 'index.html', context)

def profile(request, id):
    context = {}
    user = request.user
    posts = Post.objects.filter(user=user)
    context['user'] = user
    context['posts'] = posts
    return render(request, 'profile.html', context)
		
def post_video(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            return redirect(reverse('index'))
            
        user = request.user
        url = form.cleaned_data['url']
        title = form.cleaned_data['title']
        new_post = Post.objects.create(user=user, url=url, title=title)
        new_post.save()
        return redirect(reverse('index'))
        
		
		
		