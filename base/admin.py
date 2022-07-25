from django.contrib import admin

# Register your models here.
from .models import Room,Topic,Message

admin.site.register(Room)#to register the Room
admin.site.register(Topic)
admin.site.register(Message)

