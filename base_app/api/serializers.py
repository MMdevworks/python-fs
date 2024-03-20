#classes that take our obj and convert to json obj and return it

from rest_framework.serializers import ModelSerializer
from base_app.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'