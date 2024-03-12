from django.shortcuts import render


rooms = [
    {'id': 1, 'name': 'Strength in Numbers'},
    {'id': 2, 'name': 'Weekend Warriors'},
    {'id': 3, 'name': 'Challenge Accepted'},
]

def home(request):
    context = {'rooms': rooms}
    return render(request, 'base_app/home.html', context)

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base_app/room.html', context)
