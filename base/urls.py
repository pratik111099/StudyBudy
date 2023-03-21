from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),

    path('', views.homeView, name='home'),
    path('room/<str:pk>', views.roomView, name='room'),

    path('create_room', views.createRoomView, name='create_room'),
    path('update_room/<str:pk>', views.updateRoomView, name='update_room'),
    path('delete_room/<str:pk>', views.deleteRoomView, name='delete_room'),
    
]
