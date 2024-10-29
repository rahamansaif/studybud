from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from base import models
from base.models import User
from base.forms import RoomForm, UserForm, MyUserCreationForm


def home(request):
    q = request.GET.get('q')
    topic = request.GET.get('topic')

    template = 'base/home.html'
    topics = models.Topic.objects.all().annotate(num_rooms=Count('rooms')).order_by('-num_rooms')[:5]

    rooms = models.Room.objects.all()
    total_room_count = rooms.count()
    if topic:
        rooms = rooms.filter(topic__name=topic)
    elif q:
        rooms = rooms.filter(
            Q(name__icontains=q) |
            Q(topic__name__icontains=q) |
            Q(host__username__icontains=q)
        )
    room_count = rooms.count()

    message_feed = models.Message.objects.all().order_by('-updated_at')
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'total_room_count': total_room_count,
        'message_feed': message_feed,
    }
    return render(request, template, context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    template = 'base/login_register.html'
    page = 'login'

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # try:
        #     user = User.objects.get(username=username)
        # except User.DoesNotExist:
        #     messages.add_message(request=request, level=messages.ERROR, message='Username does not exist')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request=request, user=user)
            return redirect('home')
        messages.add_message(request=request, level=messages.ERROR, message='Wrong username or password')

    context = {'page': page}
    return render(request, template, context)


def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.add_message(request=request, level=messages.ERROR, message='An error occured')
    
    template = 'base/login_register.html'
    page = 'register'
    form = MyUserCreationForm()
    context = {
        'page': page,
        'form': form,
    }
    return render(request, template, context)


def logout_user(request):
    logout(request)
    return redirect('home')


def user_profile(request, id):
    topic = request.GET.get('topic')

    user = User.objects.get(id=id)
    template = 'base/profile.html'

    rooms = user.hosted_rooms.all()
    total_room_count = rooms.count()
    topics = models.Topic.objects.filter(rooms__in=rooms).annotate(num_rooms=Count('id')).order_by('-num_rooms')
    if topic:
        rooms = rooms.filter(topic__name=topic)

    message_feed = user.messages.all().order_by('-updated_at')
    context = {
        'user': user,
        'rooms': rooms,
        'total_room_count': total_room_count,
        'topics': topics,
        'message_feed': message_feed,
    }
    return render(request, template, context)


def room(request, id):
    room = models.Room.objects.get(id=id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            body = request.POST.get('body')
            user = request.user
            models.Message.objects.create(body=body, user=user, room=room)
            room.participants.add(user)
            return redirect('room', id=room.id)                                    ########## Why? 3:12:00
    template = 'base/room.html'
    chat_messages = room.message_set.all().order_by('-created_at')
    particpants = room.participants.all()
    context = {
        'room': room,
        'chat_messages': chat_messages,
        'participants': particpants,
    }
    return render(request, template, context)


@login_required(login_url='login')
def create_room(request):
    template = 'base/room_form.html'
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
        #     room.participants.add(request.user)
        #     return redirect('home')
        topic, created = models.Topic.objects.get_or_create(name=request.POST.get('topic'))
        room = models.Room.objects.create(
            name=request.POST.get('name'),
            topic=topic,
            host=request.user,
            description=request.POST.get('description'),
        )
        room.participants.add(request.user)
        return redirect('home')
    form = RoomForm()
    topics = models.Topic.objects.all()
    context = {'form': form, 'topics': topics}
    return render(request, template, context)


@login_required(login_url='login')
def update_room(request, id):
    template = 'base/room_form.html'
    room = models.Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('You are not allowed to be here!!')
    
    if request.method == 'POST':
        topic, created = models.Topic.objects.get_or_create(name=request.POST.get('topic'))
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    form = RoomForm(instance=room)
    topics = models.Topic.objects.all()
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, template, context)


@login_required(login_url='login')
def delete_room(request, id):
    template = 'base/delete.html'
    room = models.Room.objects.get(id=id)

    if request.user != room.host:
        return HttpResponse('You are not allowed to be here!!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, template, context)


@login_required(login_url='login')
def delete_message(request, id):
    template = 'base/delete.html'
    message = models.Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('You are not allowed to be here!!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request, template, context)


@login_required(login_url='login')
def edit_message(request, id):
    template = 'base/edit_message.html'
    message = models.Message.objects.get(id=id)

    if request.user != message.user:
        return HttpResponse('You are not allowed to be here!!')
    
    if request.method == 'POST':
        message_body = request.POST.get('body')
        message.body = message_body
        message.save()
        return redirect('home')
    context = {'message': message}
    return render(request, template, context)


@login_required(login_url='login')
def update_user(request):
    template = 'base/update_user.html'
    if request.method == 'POST':
        form = UserForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('user-profile', request.user.id)
    form = UserForm(instance=request.user)
    context = {'form': form}
    return render(request, template, context)


def topics_page(request):
    template = 'base/topics.html'
    q = request.GET.get('q') or ''
    topics = models.Topic.objects.filter(name__icontains=q).annotate(num_rooms=Count('rooms')).order_by('-num_rooms')
    total_room_count = models.Room.objects.all().count()
    context = {
        'topics': topics,
        'total_room_count': total_room_count,
    }
    return render(request, template, context)


def activity_page(request):
    template = 'base/activity.html'
    message_feed = models.Message.objects.all().order_by('-updated_at')[:4]
    context = {
        'message_feed': message_feed,
    }
    return render(request, template, context)
