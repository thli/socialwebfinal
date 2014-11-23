from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.		
class Profile(models.Model):
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return unicode(self.user)

class Post(models.Model):
    user = models.ForeignKey(Profile)
    url = EmbedVideoField()
    title = models.CharField(max_length=40)
    liked = models.ManyToManyField(Profile, related_name="likedby")

    @property
    def likes(self):
        return self.liked.count()

    def __unicode__(self):
        return self.url
        
class Tag(models.Model)
    tag = models.CharField(max_length=20)
    posts = models.ManyToManyField(Post)
    
    def __unicode__(self):
        return self.tag