from django.shortcuts import render,redirect
# from django.http import HttpResponse
from .models import Room,Topic
from .forms import Roomform
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages

def login(request):

    # if request.method=="POST":
    #     username=request.POST.get('username')
    #     password=request.POST.get('password')

    #     try:
    #         user = User.objects.get(username=username)
    #     except:
    #         messages.error(request, "Document deleted.")

    context = {{'username':username}}

    return render(request,'baseapp/login_register.html',context)

def home(request):

    if request.GET.get('q') != None :
        q = request.GET.get("q")
    else:
        q=''
    room = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)
        )
    topic= Topic.objects.all()
    room_count = room.count()
    context ={'room':room,'topic':topic,'q':q,'room_count':room_count}
    return render(request,'baseapp/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    
    return render(request,'baseapp/room.html',{'room':room})

def createRoom(request):
    form = Roomform()
    if request.method == "POST":
        form = Roomform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'baseapp/create_room.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)
    if request.method == "POST":
    # why we add instance means for update in same room .
    # if we not added instance IT WILL CREATE NEW ROOM
        form = Roomform(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'baseapp/create_room.html',context)
    
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request,'baseapp/delete_room.html',context)
    
# Create your views here.
