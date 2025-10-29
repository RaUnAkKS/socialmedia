from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True,blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    location = models.CharField(max_length=100)
    dob = models.DateField(null=True , blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='person')
    image = models.ImageField(null=False)
    caption = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')

class Engagement(models.Model):
    viewer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='viewer',null=True,blank=True)
    like = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='like',null=True,blank=True)
    comment = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comment',null=True,blank=True)
    comment_text = models.TextField(max_length=500,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

class StoryPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class Message(models.Model):
    user1 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    user2 = models.ForeignKey(User,on_delete=models.CASCADE,related_name='receiver')
    text = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
