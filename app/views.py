from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .models import User,Post,Follow,Engagement,StoryPost,Message
from .forms import MyUserCreationForm,PostForm,UpdateForm,StoryPostForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
   
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        following_ids = Follow.objects.filter(follower=request.user).values_list('following__id',flat=True)
        posts = Post.objects.filter(user__in=list(following_ids) + [request.user.id])
        liked_post_ids = Engagement.objects.filter(viewer=request.user).values_list('like__id',flat=True)
        all_story = StoryPost.objects.filter(user__in=list(following_ids)+[request.user.id])
        user_chat = User.objects.filter( Q(sender__user2=request.user) | Q(receiver__user1=request.user)).distinct()[0:3]
        context = {'posts':posts,'liked_post_ids':liked_post_ids,'all_story':all_story,'user_chat':user_chat}
        return render(request,'app/home.html',context)
    else:
        messages.error(request,'Login or Register to see the Feed')
        return render(request,'app/home.html')

def login_page(request):
    page = 'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return render(request,'app/home.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return render(request,'app/login_register.html',context)
    return render(request,'app/login_register.html',context)

def logout_page(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Input')

    return  render(request,'app/login_register.html',{'form':form})

def post_page(request):
    form = PostForm()
    context = {'form':form}
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
        else:
            messages.error(request,'Something is wrong in the post')

    return render(request,'app/post.html',context)

def story_post_page(request):
    form = StoryPostForm()
    story = 'story'
    context = {'form':form,'story':story}
    if request.method == 'POST':
        form = StoryPostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
        else:
            messages.error(request,'Something is wrong in the post')

    return render(request,'app/post.html',context)

def story_page(request,pk):
    post = Post.objects.filter(id=pk).first()
    context = {'post':post}
    return render(request,'app/story.html',context)

def profile_page(request,pk):
    user = User.objects.get(id=pk)
    post = Post.objects.filter(user=user)
    following_ornot = Follow.objects.filter(follower=request.user,following=user).first()
    context = {'posts':post,'owner':user,'following_ornot':following_ornot}
    return render(request,'app/profile.html',context)

def update_page(request):
    update_form = UpdateForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    context = {'update_form':update_form,'password_form':password_form}
    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = UpdateForm(request.POST,request.FILES,instance=request.user)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                messages.success(request,'Updated Succesfully')
                return redirect('profile',pk=request.user.id)
            else:
                messages.error(request,'Somethig Invalid!')
        else:
            form = PasswordChangeForm(request.user,request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # keeps user logged in
                messages.success(request, 'Password changed successfully!')
                return redirect('profile')

    return render(request,'app/update.html',context)

def follow_unfollow_page(request,pk):
    if request.method == 'POST':
        profile_user = User.objects.get(id=pk)
        requested_user = request.user
        if profile_user == requested_user:
            return redirect('home')
        
        existing_follow = Follow.objects.filter(follower=requested_user,following=profile_user).first()

        if existing_follow:
            existing_follow.delete()
        else:
            Follow.objects.create(follower=requested_user,following=profile_user)
        return redirect('profile',pk=profile_user.id)

def search_page(request):
    name = request.GET.get('q')
    user = User.objects.filter(username=name).first()
    if user is None:
        messages.error(request,'No user found')
        return redirect('home')
    else:
        return redirect('profile',pk=user.id)
    
def engagement_page(request,pk):
    liking_person = request.user
    post = Post.objects.get(id=pk)
    if 'like' in request.POST:
        liked_ornot = Engagement.objects.filter(viewer=liking_person,like=post)
        if liked_ornot:
            liked_ornot.delete()
            messages.success(request,'Unliked Successfully')
            return redirect('home')
        else:
            Engagement.objects.create(viewer=liking_person,like=post)
            messages.success(request,'Liked Successfully')
            return redirect('home')
    else:
            post = Post.objects.get(id=pk)
            commented_users = Engagement.objects.filter(comment=pk)
            context = {'commented_users':commented_users,'post':post}
            if 'text' in request.POST:
                text_received = request.POST.get('text').strip()
                if text_received:
                    Engagement.objects.create(viewer=liking_person,comment=post,comment_text=request.POST.get('text'))
                    messages.success(request,'Commented Successfully')
                else:
                    messages.error(request,'Invalid Input!')

            return render(request,'app/comment.html',context)
        
def like_detail_page(request,pk):
    liked_users = Engagement.objects.filter(like=pk)
    context = {'liked_users':liked_users}
    return render(request,'app/like.html',context)

def message_page(request):
    user_chat = User.objects.filter( Q(sender__user2=request.user) | Q(receiver__user1=request.user)).distinct()
    msg = Message.objects.filter(Q(user1__in=user_chat,user2=request.user)|Q(user2__in=user_chat,user1=request.user))
    context = {'user_chat':user_chat,'msg':msg}
    return render(request,'app/message.html',context)

def chat_page(request,pk):
    other_person = User.objects.filter(id=pk).first()
    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg.strip():
            Message.objects.create(user1=request.user,user2=other_person,text=msg)
        return redirect('chat',pk=pk)
    all_conversation = Message.objects.filter(Q(user1=request.user,user2__id=pk)|Q(user1__id=pk,user2=request.user))
    context = {'all_conversation':all_conversation,'other_person':other_person}
    return render(request,'app/chats.html',context)

def search_user_page(request):
    name = request.GET.get('q').strip()
    if name == '':
        messages.error(request,'Invalid Input!')
        return redirect('home')
    all_user = User.objects.filter(username__icontains=name)
    context = {'all_user':all_user}
    return render(request,'app/search_user.html',context)

def follow_user_page(request, pk):
    user = User.objects.get(id=pk)
    name_param = request.GET.get('name', '')

    if name_param == 'follower':
        follows = User.objects.filter(follower__following=user)
        name = "Followers"
    else:
        follows = User.objects.filter(following__follower=user)
        name = "Following"

    context = {'follows': follows, 'name': name, 'user': user}
    return render(request, 'app/follower_following.html', context)
