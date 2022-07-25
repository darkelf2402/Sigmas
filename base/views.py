from email import message
from multiprocessing import context
from pydoc_data.topics import topics
from unicodedata import name
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required # to restrict some pages if no login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Message, Room,Topic,Message
from .forms import RoomForm,UserForm
from django.db.models import Q

#models have id given out to them by default

# Create your views here.

# rooms=[
#         {'id':1,'name':'learning django'},
#         {'id':2,'name':'learning django lik a boss'},
        
# ]


def loginPage(request):
    
    page ='login'
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':# if data has been entered
        username = request.POST.get('username')
        password = request.POST.get('password')
        
    else:# or else it shows an error
        username = request.POST.get('')
        password = request.POST.get('')
        
        
    # try:                                              # to check whether the user exists or no
    #     user = User.object.get(username = username)
    # except:
        
    #     messages.error(request,'User illa , tm Hogu')
        
    user = authenticate(request,username=username,password=password) # to authenticate user
    
    if user is not None:
        login(request,user)
        return redirect('home')
    else:
        messages.error(request,'Username or password does not exist')
        
    
    context = {'page':page}
    return render(request,'base/loginbro.html',context)


def logoutPage(request):
    logout(request)
    return redirect('home')

def registeruser(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)# to input all the data from register
        if form.is_valid():
            user = form.save(commit=False) # to create that user as object
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Damn!!!!')
            
            
    return render(request,'base/loginbro.html',{'form' : form})

def home(request):# urls files are for routuing
    q = request.GET.get('q') if request.GET.get('q')!=None else '' # (acts as a search bar)checks for that topic name and prints stuff related to that topic
    
    rooms = Room.objects.filter(
                                Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q) # Q allows you to add or/and statements to search 
                                
                                )
    room_count = rooms.count()
    
    topics = Topic.objects.all()
    messages = Message.objects.filter(Q(room__topic__name__icontains=q)) # gives recent activity only of the room selected
    context = {'rooms' : rooms , 'topics':topics , 'room_count':room_count,
               'messages':messages}#to acess all topics to list them first import Topic from model then call all items then render in home.html
    
    return render(request,'base/home.html',context)



def room(request,pk):
    room = Room.objects.get(id = pk) # using get to just get 1 value from the key
    messages = room.message_set.all().order_by('-created') # one to many- to take all the message message is a child of room
    participants = room.participants.all() #many to many
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
    
    context = {'room' : room , 'messages':messages,'participants':participants}
    return render(request,'base/room.html',context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)# go to the user with that id
    rooms = user.room_set.all()
    messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,'rooms':rooms,'messages':messages,'topics':topics}
    return render(request,'base/profile.html',context)

@login_required(login_url='login')
def createroom(request):#to create new room
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':
        #print(request.POST) #getiing input from form and print request.post is printing it 
        # request.POST.get('name')#it can be used to get name or anything else
        # form = RoomForm(request.POST)# getting all data from form
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)# it sees whether the entered topic is there or not and creates a new on eif ithe topic is new
        # if form.is_valid():
                            #form.save()
        Room.objects.create(
        host = request.user,
        topic = topic,
        name = request.POST.get('name'),
        description = request.POST.get('description'),                
                )
            # room = form.save() # this creates a instance of room
            # room.host = request.user
            # room.save()
            # room.participants.add(request.user)
        return redirect('home')#home is name not url
        
        
            
    context = {'form':form , 'topics':topics}
    return render(request,'base/room_form.html',context) 


@login_required(login_url='login')
def updateroom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)#intial value of form will already be present
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse('Get the F out of here')
    
    if request.method == 'POST':
        # form = RoomForm(request.POST, instance=room)#instance gets the original value for it to update , if no instance it will create another room
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')#home is name not url
        
    context = {'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)



@login_required(login_url='login')
def deleteroom(request,pk):
    room = Room.objects.get(id = pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    if request.user != room.host:
        return HttpResponse('Get the F out of here')
    
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url='login')
def deletemessage(request,pk):
    message = Message.objects.get(id = pk)
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    if request.user != message.user:
        return HttpResponse('Get the F out of here')
    
    return render(request,'base/delete.html',{'obj':message})
    
    

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile',pk=user.id)
        
    
    return render(request,'base/update-user.html',{'form':form})


def topicsPage(request):
    return render(request,'base/topics.html',{})
    
    
def activityPage(request):
    room_messages = Message.objects.all() #Here getting all the messages  
    return render(request,'base/activity.html',{})
