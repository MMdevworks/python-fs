from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' # will create form based on the metadata in models.py
        exclude = ['host', 'participants'] #excluded fields for form

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
