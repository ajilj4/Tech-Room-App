from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic, Message
from .forms import Roomform
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm

def loginpage(request):
    page = "login"
    if request.method=="POST":

        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            redirect('home')
            
        except:
            messages.error(request, "Document deleted.")

        users = authenticate(request, username=username, password=password)
        if users is not None:
            login(request, users)
            return redirect('home')
        else:
            messages.error(request, "wrong info ...")
    context = {"page":page}

    return render(request,'baseapp/login_register.html',context)

def logoutpage(request):
    logout(request)
    return redirect('home')

def registerpage(request):
    page = "register"
    form= UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('home')
        else:
            messages.error(request,"an error acqure")

    context = {"page":page, "form": form}
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
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
    return render(request,'baseapp/room.html',{'room':room,'room_messages':room_messages,'participants':participants})

@login_required(login_url='/loginpage')
def createRoom(request):
    form = Roomform()
    if request.method == "POST":
        form = Roomform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'baseapp/create_room.html',context)

@login_required(login_url='/loginpage')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed")

    if request.method == "POST":
    # why we add instance means for update in same room .
    # if we not added instance IT WILL CREATE NEW ROOM
        form = Roomform(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'baseapp/create_room.html',context)


@login_required(login_url='/loginpage') 
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request,'baseapp/delete_room.html',context)


@login_required(login_url='/loginpage')
def deleteMessage(request,pk):
    delete_msg = Message.objects.get(id=pk)
    
    if request.user != delete_msg.user:
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        delete_msg.delete()
        return redirect("home")
    context = {}
    return render(request,'baseapp/delete_room.html',context)
    
# Create your views here.
