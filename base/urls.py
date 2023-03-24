from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.homeView, name='home'),
    path('room/<str:pk>', views.roomView, name='room'),
    path('profile/<str:pk>', views.userProfileView, name='profile'),

    path('create_room', views.createRoomView, name='create_room'),
    path('update_room/<str:pk>', views.updateRoomView, name='update_room'),
    path('delete_room/<str:pk>', views.deleteRoomView, name='delete_room'),
    path('delete-message/<str:pk>', views.deleteMessageView, name='delete-message'),
    
    path('update_user/<str:pk>', views.updateUserView, name='update_user'),

    path('browse_topic/', views.browseTopic, name='browse_topic'),
    path('browse_activity/', views.browseActivity, name='browse_activity'),
]
