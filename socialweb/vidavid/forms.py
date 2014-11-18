from django import forms
from models import *

from django.contrib.auth.models import User

class LoginForm(forms.Form):
	l_username = forms.CharField(max_length = 20, label = "Username",
															widget = forms.TextInput(
															attrs={'class':'input-xlarge',
															'placeholder':'Username',
															'required':'',
															'autofocus':''}))
	l_password = forms.CharField(max_length = 200, label = "Password",
															widget = forms.PasswordInput(
															attrs={'class':'input-xlarge',
															'placeholder':'Password',
															'required':''}))


class RegistrationForm(forms.Form):
	r_email = forms.CharField(max_length = 200, label = "Email",
															widget = forms.EmailInput(
															attrs={'class':'input-xlarge',
															'placeholder':'Email Address',
															'required':''}))
	r_username = forms.CharField(max_length = 20, label = "Username",
															widget = forms.TextInput(
															attrs={'class':'input-xlarge',
															'placeholder':'Username',
															'required':''}))
	r_password1 = forms.CharField(max_length = 200, label = "Password",
															widget = forms.PasswordInput(
															attrs={'class':'input-xlarge',
															'placeholder':'Password',
															'required':''}))
	r_password2 = forms.CharField(max_length = 200, label = "Confirm Password",
															widget = forms.PasswordInput(
															attrs={'class':'input-xlarge',
															'placeholder':'Confirm Password',
															'required':''}))

	def clean(self):
			cleaned_data = super(RegistrationForm, self).clean()

			# Confirms that the two password fields match
			password1 = cleaned_data.get('r_password1')
			password2 = cleaned_data.get('r_password2')
			if password1 and password2 and password1 != password2:
					raise forms.ValidationError("Passwords did not match.")

			# Generally return the cleaned data we got from our parent.
			return cleaned_data

	# Customizes form validation for the email field.
	def clean_email(self):
			# Confirms that the email is not already present in the
			# User model database.
			email = self.cleaned_data.get('email')
			if User.objects.filter(email__exact=email):
					raise forms.ValidationError("Email is already registered.")

			# Generally return the cleaned data we got from the cleaned_data
			# dictionary
			return email	
			
	# Customizes form validation for the username field.
	def clean_username(self):
			# Confirms that the username is not already present in the
			# User model database.
			username = self.cleaned_data.get('username')
			if User.objects.filter(username__exact=username):
					raise forms.ValidationError("Username is already taken.")

			# Generally return the cleaned data we got from the cleaned_data
			# dictionary
			return username
			
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'name']
        labels = {
            'url' : 'URL',
            'name' : 'Name',
        }
        widgets = {
            'url' : forms.URLInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'URL'
            }),
            'name' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Name'
            }),
        }