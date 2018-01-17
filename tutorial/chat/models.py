from django.db import models
from django.utils import timezone


class Room(models.Model):
    """
    A room object has a name attribute, telling you the name of the room, and a label
    attribute, which is unique for every room object.
    """
    name = models.TextField()
    label = models.SlugField(unique=True)


class Message(models.Model):
    """
    A message object relates to a room object and contains text in its handle and
    message attributes. The timestamp attribute marks the creation time.
    """
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.PROTECT)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
