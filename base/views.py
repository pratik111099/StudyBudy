from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

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
    pagename = 'register'
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print('0')
        if form.is_valid():
            print('1')
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            print(user)
            login(request, user)
            return redirect('home') 
        
        else:
            messages.error(request, 'An error occured during registration')

    context = {
            'pagename':pagename,
            'form':form,
        }
    return render(request, 'base/login_registration.html', context)


def homeView(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
                Q(topic__name__icontains=q) |
                Q(name__icontains=q) |
                Q(description__icontains=q)  
        )
    topics = Topic.objects.all()
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
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponse("Error")
    context = {
        'form':form
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def updateRoomView(request, pk):
    room = Room.objects.get(id=int(pk))
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here.')
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return HttpResponse("Error")
    context = {
        'form':form,
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
        return redirect('home')
    
    context = {
        'room':message
    }
    return render(request, 'base/delete.html', context)