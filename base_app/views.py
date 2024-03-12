from django.shortcuts import render
from .models import Room

# rooms = [
#     {'id': 1, 'name': 'Strength in Numbers'},
#     {'id': 2, 'name': 'Weekend Warriors'},
#     {'id': 3, 'name': 'Challenge Accepted'},
# ]

def home(request):
    #will give us all obj in db
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base_app/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base_app/room.html', context)

def createRoom(request):
    context = {}
    return render(request, 'base_app/room_form.html', context)