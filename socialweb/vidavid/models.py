from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PostManager(models.Manager):
	def create_post(self, user, url):
		post = self.create(user=user,url=url)
		return post
		
class Post(models.Model):
	user = models.ForeignKey(User)
	url = models.CharField(max_length = 200, blank = False, null = False)
	objects = PostManager()