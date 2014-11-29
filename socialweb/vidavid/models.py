from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

# Create your models here.		
class Profile(models.Model):
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    description = models.CharField(max_length=400)
    picture = models.ImageField(upload_to='profile', blank=True, default='profile/default.png')
    
    @property
    def name(self):
        return self.firstname + " " + self.lastname
    
    def __unicode__(self):
        return unicode(self.user)

class Tag(models.Model):
    tag = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.tag        

class Post(models.Model):
    user = models.ForeignKey(Profile)
    url = EmbedVideoField()
    title = models.CharField(max_length=40)
    liked = models.ManyToManyField(Profile, related_name="likedby")
    tags = models.ManyToManyField(Tag)

    @property
    def likes(self):
        return self.liked.count()

    def __unicode__(self):
        return self.url
        
