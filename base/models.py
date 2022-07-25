
from django.db import models
from django.contrib.auth.models import User
from sqlalchemy import true

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200) # topic not more than 200 charecters
    
    def __str__(self):
        return self.name# passing the name back
    


class Room(models.Model):
    
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True , blank = True)# null=True maens this can be empty
    participants =models.ManyToManyField(User,related_name='participants',blank=True)
    updated = models.DateTimeField(auto_now=True) # to take timestamp whenever its updted
    created = models.DateTimeField(auto_now_add=True) # auto_now_add only updates first time
    host = models.ForeignKey(User,on_delete=models.SET_NULL , null=True )
    
    
    def __str__(self):
        return self.name
    
    
    class Meta: #done inside room such that the newest items are at top
        ordering = ['-updated','-created']#last goes to first

        def __str__(self):
            return self.name
    

    
class Message(models.Model): # these are basically children of Room class 
    user = models.ForeignKey(User,on_delete=models.CASCADE , null=True ) # user can have many messages but a message can have only one user
    room = models.ForeignKey(Room,on_delete=models.CASCADE)# once room deleted all messages from that room deleted using cascade
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) # to take timestamp whenever its updted
    created = models.DateTimeField(auto_now_add=True) # auto_now_add only updates first time
    
    def __str__(self):
        return self.body[0:50]
    
    
    class Meta: #done inside room such that the newest items are at top
        ordering = ['-updated','-created']#last goes to first

        def __str__(self):
            return self.name
    
    
    
    
    