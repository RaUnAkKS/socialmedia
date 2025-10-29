from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Post,Engagement,StoryPost
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
User = get_user_model()

class MyUserCreationForm(UserCreationForm):
    class Meta:     
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2' , 'location' , 'dob']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['image' , 'caption']

class UpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username' , 'email' , 'location' , 'dob' , 'bio' , 'avatar']

class StoryPostForm(ModelForm):
    class Meta:
        model = StoryPost
        fields = ['image']