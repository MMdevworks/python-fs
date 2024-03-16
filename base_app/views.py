from django.shortcuts import render, redirect
from  django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User

# rooms = [
#     {'id': 1, 'name': 'Strength in Numbers'},
#     {'id': 2, 'name': 'Weekend Warriors'},
#     {'id': 3, 'name': 'Challenge Accepted'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try: 
            User.objects.get(username=username)
        except:
            messages.error(request, "User not found.")
            #https://docs.djangoproject.com/en/5.0/ref/contrib/messages/

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist.")

    context={'page': page}
    return render(request, 'base_app/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower() #update users created name to lower so case insensitive
            user.save()
            login(request, user) #login and send home
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred. Check username and password')
    context = {'form': form}
    return render(request, 'base_app/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    #https://docs.djangoproject.com/en/5.0/topics/db/queries/
    #https://docs.djangoproject.com/en/5.0/ref/models/querysets/
    #search queries
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))

    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}

    return render(request, 'base_app/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() #message = Message class model
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {
        'room': room, 
        'room_messages': room_messages, 
        'participants': participants
        }
    return render(request, 'base_app/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user, 
        'rooms': rooms, 
        'room_messages': room_messages,
        'topics': topics
        }
    return render(request, 'base_app/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base_app/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Only the room creator may make changes')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base_app/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Only the room creator may make changes')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base_app/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Only the room creator may make changes')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base_app/delete.html', {'obj': message})