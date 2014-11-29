from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404

from mimetypes import guess_type

from vidavid.models import *
from vidavid.forms import *
from django import forms
import json

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

        # Creates the new user and profile from the valid form data
        new_user = User.objects.create_user(username=r_form.cleaned_data['r_username'],
                        email=r_form.cleaned_data['r_email'],
                        password=r_form.cleaned_data['r_password1'])

        new_user.save()
        new_profile = Profile(user=new_user)
        new_profile.save()
        
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
#                      Template views                         #
#-------------------------------------------------------------#
    
def index(request):
    context = {}
    user = get_object_or_404(Profile, user=request.user)
    posts = Post.objects.all().order_by('-id')[:10]
    context['posts'] = posts	
    context['post_form'] = PostForm()
    context['search_form'] = SearchForm()
    return render_to_response('index.html', context, context_instance=RequestContext(request))

def profile(request, id):
    context = {}
    context['post_form'] = PostForm()
    context['search_form'] = SearchForm()
    profile = get_object_or_404(Profile, id=id)
    posts = Post.objects.filter(user=profile)
    context['posts'] = posts
    
    tags = set()
    all_tags = Tag.objects.all()
    for tag in all_tags:
        for post in posts:
            if post.tags.filter(tag=tag).exists():
                tags.add(tag)
    context['tags'] = tags
   
    context['profile'] = profile
    return render_to_response('profile.html', context, context_instance=RequestContext(request))    
    
def search(request):
    context = {}
    context['post_form'] = PostForm()
    context['search_form'] = SearchForm()
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if not form.is_valid():
            #error nothing could be found
            return render_to_response('search.html', context, context_instance=RequestContext(request))
        query = form.cleaned_data['query']
        posts = set()
        for tag in Tag.objects.all():
            for post in Post.objects.all():
                if post.tags.filter(tag=query).exists():
                    posts.add(post)
                    
        context['posts'] = posts
    return render_to_response('search.html', context, context_instance=RequestContext(request))      

def edit_profile(request):
    context = {}
    context['search_form'] = SearchForm()
    context['password_form'] = PasswordForm()
    profile = get_object_or_404(Profile, user=request.user)
    context['profile'] = profile
    if request.method == 'GET':
        context['edit_form'] = EditProfileForm(instance=profile)
    if request.method == 'POST':
        edit_form = EditProfileForm(request.POST, request.FILES)
        context['edit_form'] = edit_form
        if not edit_form.is_valid():
            messages.error(request, 'Form incorrectly completed. Please try again.')
            return render_to_response('edit.html', context, context_instance=RequestContext(request))
        profile.firstname = edit_form.cleaned_data['firstname']
        profile.lastname = edit_form.cleaned_data['lastname']
        profile.description = edit_form.cleaned_data['description']
        if 'picture' in request.FILES:
            profile.picture = edit_form.cleaned_data['picture']
        profile.save()
        messages.success(request, 'Saved changes.')
    return render_to_response('edit.html', context, context_instance=RequestContext(request))
    
#-------------------------------------------------------------#
#                           Actions                           #
#-------------------------------------------------------------#    
    
def update_index(request):
    id = request.GET.get("min_id")
    posts = Post.objects.filter(id__lt=id).order_by('-id')[:5]
    data = json.dumps(render_to_string('post-list-snippet.html', {'posts': posts}, 
                                    context_instance=RequestContext(request)))
    return HttpResponse(data, content_type='application/json')
    
def post_video(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if not form.is_valid():
            return redirect(reverse('index'))
            
        user = get_object_or_404(Profile, user=request.user)
        url = form.cleaned_data['url']
        title = form.cleaned_data['title']
        tags = form.cleaned_data['tags'].split(",")
        new_post = Post.objects.create(user=user, url=url, title=title)          

        for new_tag in tags:
            tag, created = Tag.objects.get_or_create(tag=new_tag)
            tag.save()
            new_post.tags.add(tag)
            
        new_post.save()
        return redirect(reverse('index'))
        
def like_post(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        user = get_object_or_404(Profile, user=request.user)
        post = get_object_or_404(Post, id=id)
        post.liked.add(user)
        post.save()
        return HttpResponse(post.likes)
        
    return Http404

def delete_post(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        user = get_object_or_404(Profile, user=request.user)
        post = get_object_or_404(Post, id=id)
        if not (post.user == user):
            #trying to delete another user's post?
            return Http404
        post.delete()
        return HttpResponse()

def update_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Passwords do not match.')
            return redirect(reverse('edit'))
            
        user = request.user
        if user.check_password(form.cleaned_data['current_password']):
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            user = authenticate(username=user.username,
                password=form.cleaned_data['new_password1'])
            login(request, user)
            messages.success(request, 'Password saved.')
        return redirect(reverse('edit'))
        
#-------------------------------------------------------------#
#                           Utility                           #
#-------------------------------------------------------------#       
        
def get_profile_photo(request, id):
    profile = get_object_or_404(Profile, id=id)
    if not profile.picture:
        raise Http404
    content_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=content_type)
