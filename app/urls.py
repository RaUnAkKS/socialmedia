from django.urls import path
from .import views

urlpatterns = [
    path('',views.home, name="home"),
    path('login/',views.login_page,name="login"),
    path('logout/',views.logout_page,name="logout"),
    path('register/',views.register_page,name="register"),
    path('post/',views.post_page,name="post"),
    path('story_post/',views.story_post_page,name="story_post"),
    path('story/<str:pk>/',views.story_page,name="story"),
    path('profile/<str:pk>/',views.profile_page,name="profile"),
    path('update/',views.update_page,name="update"),
    path('follow_unfollow/<str:pk>/',views.follow_unfollow_page,name="follow_unfollow"),
    path('search/',views.search_page,name="search"),
    path('engagement/<str:pk>/',views.engagement_page,name="engagement"),
    path('like_detail/<str:pk>/',views.like_detail_page,name="like_detail"),
    path('message/',views.message_page,name="message"),
    path('chat/<str:pk>/',views.chat_page,name="chat"),
    path('search_user/', views.search_user_page,name="search_user"),
    path('follow_user/<str:pk>/', views.follow_user_page,name="follow_user"),
]