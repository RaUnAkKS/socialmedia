from django.contrib import admin

# Register your models here.
from .models import User,Post,Follow,Engagement,StoryPost,Message

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Follow)
admin.site.register(Engagement)
admin.site.register(StoryPost)
admin.site.register(Message)
