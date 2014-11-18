from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.		
class Profile(models.Model):
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return user

class Post(models.Model):
    user = models.ForeignKey(User)
    url = EmbedVideoField()
    title = models.CharField(max_length=40)
#    tags = models.

    def __unicode__(self):
        return url
        
        