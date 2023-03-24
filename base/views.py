from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.
def loginUser(request):
    pagename = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User is not exit.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password not exit.')

    context = {
        'pagename':pagename,
    }
    
    return render(request, 'base/login_registration.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            print(user)
            login(request, user)
            return redirect('home') 
        
        else:
            messages.error(request, 'An error occured during registration')

    context = {
            'form':form,
        }
    return render(request, 'base/signup.html', context)


def homeView(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
                Q(topic__name__icontains=q) |
                Q(name__icontains=q) |
                Q(description__icontains=q)  
        )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {
        'rooms':rooms,
        'topics':topics,
        'room_count':room_count,
        'room_message':room_message,
    }
    return render(request,'base/home.html', context)



def roomView(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        comment = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('msg')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room':room,
        'room_messages':room_messages,
        'participants':participants,
    }
    return render(request, 'base/room.html', context)



def userProfileView(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    room_message = user.message_set.all()

    context = {
        'user': user,
        'rooms': rooms,
        'topics':topics,
        'room_message':room_message,
    }
    return render(request, 'base/profile.html', context)



@login_required(login_url='/login')
def createRoomView(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
        
    context = {
        'form':form,
        'topics':topics,
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoomView(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here.')
    
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
      
    context = {
        'form':form,
        'room':room,
        'topics':topics,
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def deleteRoomView(request, pk):
    room = Room.objects.get(id=int(pk))

    if request.user != room.host:
        return HttpResponse('You are not allowed here.')
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {
        'room':room
    }
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def deleteMessageView(request, pk):
    message = Message.objects.get(id=int(pk))

    if request.user != message.user:
        return HttpResponse('You are not allowed here.')
    
    if request.method == "POST":
        message.delete()
        return redirect('room', pk=message.room.id)
    
    context = {
        'room':message
    }
    return render(request, 'base/delete.html', context)

@login_required(login_url='login')
def updateUserView(request, pk):
    user = User.objects.get(id=pk)
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return redirect('profile', user.id)

    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'base/edit_user.html', context)

def browseTopic(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    return render(request, 'base/topics.html', {'topics': topics})

def browseActivity(request):
    room_message = Message.objects.all()[0:3]
    return render(request, 'base/activity.html', {'room_message': room_message})