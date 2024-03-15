from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__' # will create form based on the metadata in models.py
        exclude = ['host', 'participants'] #excluded fields for form