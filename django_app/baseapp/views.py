from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic, Message,User
from .forms import Roomform,Userform, MyUserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.forms import UserCreationForm

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
    form= MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
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
    # q= request.GET.get('q') if request.GET.get('q') != None else ""
    room = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)

        )
    topic= Topic.objects.all()
    recent_msg = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by("-id")[:4]
    room_count = room.count()
    context ={'room':room,'topic':topic,'q':q,'room_count':room_count,"recent_msg":recent_msg }
    return render(request,'baseapp/home.html',context)

def room(request,pk):
    page = 'room'
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
    
    return render(request,'baseapp/room.html',{'room':room,'room_messages':room_messages,'participants':participants,'page':page})

def userprofile(request,pk):
    # recent_msg = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by("-id")[:2]
    page= "profile"
    user = User.objects.get(id=pk)
    topic = Topic.objects.all()
    room = user.room_set.all()
    recent_msg = user.message_set.all()

    context = {'user':user,'topic':topic,'room':room,'recent_msg':recent_msg,'page':page}
    return render(request,'baseapp/profile.html',context)



@login_required(login_url='/loginpage')
def createRoom(request):
    page= "create"
    form = Roomform()
    topic= Topic.objects.all()
    if request.method == "POST":
        topic = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context = {'form':form ,'topic':topic,'page':page}
    return render(request,'baseapp/create_room.html',context)

@login_required(login_url='/loginpage')
def updateRoom(request,pk):
    page= 'update'
    room = Room.objects.get(id=pk)
    form = Roomform(instance=room)
    topics= Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse("You are not allowed")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
    # why we add instance means for update in same room .
    # if we not added instance IT WILL CREATE NEW ROOM
        # form = Roomform(request.POST,instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
    context = {'form':form ,'topic':topics,'page':page}
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


@login_required(login_url='login')
def updateUser(request):
    user = request.user

    form = Userform(instance=user)
    if request.method == 'POST':
        form = Userform(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
        return redirect('profile',pk=user.id)
    return render(request, 'baseapp/updateProfile.html', {'form': form})


def topic(request) :
    q= request.GET.get('q') if request.GET.get('q') != None else ""
    topic = Topic.objects.filter(Q(name__icontains=q))
    return render(request,'baseapp/topic.html',{'topic':topic})

    
# Create your views here.
