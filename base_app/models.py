from django.db import models
from django.contrib.auth.models import User

#room will be a child of a topic

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) #need to set null to true to ensure db will alow the null value
    name = models.CharField(max_length=200)
    #null means database can't have an instance of this model with this being blank, null is default False, so we set it to true so that it can be blank
    # same for blank, blank is for form validation, if it's empty then ok
    description = models.TextField(null=True, blank=True) 
    # participants =
    updated = models.DateTimeField(auto_now=True) #for timestammp on save
    created = models.DateTimeField(auto_now_add=True) #timestap only on create

    class Meta:
        ordering = ['-updated', '-created'] # order in reverse 

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #one to many
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #one to many #CASCADE- if deleted, its children get deleted
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50] #preview first 50 characters
