from django.urls import path
from . import views



urlpatterns=[
    path('loginpage/',views.loginpage,name='loginpage'),
    path('logoutpage/',views.logoutpage,name='logoutpage'),
    path('registerpage/',views.registerpage,name='registerpage'),

    path('',views.home,name='home'),
    path('profile/<str:pk>',views.userprofile,name='profile'),
    path('room/<str:pk>',views.room,name='room'),

    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>',views.deleteMessage,name='delete-message'),
    
    path('topic/',views.topic,name='topic'),
    path('recent/',views.recent,name='recent'),
    path('update-user/',views.updateUser,name='update-user'),
]