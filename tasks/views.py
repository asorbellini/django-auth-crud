from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate 
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .forms import CreateTaskForm
from .models import Tasks

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{
        'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html',{
            'form': UserCreationForm,
            'error' : 'Username already exists.'
        })
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            'error' : 'Password do no match'
        })
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user == None:
            return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect.'
        })
        else:
            login(request, user) 
            return redirect('tasks')
   
def signout(request):
    logout(request)
    return redirect('home')
@login_required
def tasks(request):
    tasks = Tasks.objects.filter(user = request.user, datecomplete__isnull=True)
    return render(request,'tasks.html', {
        'tasks': tasks
    })
@login_required
def tasks_completed(request):
    tasks = Tasks.objects.filter(user = request.user, datecomplete__isnull=False).order_by('-datecomplete')
    return render(request,'tasks.html', {
        'tasks': tasks
    })
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'create_task.html',{
            'form': CreateTaskForm
        })
    else:
        try:
            form = CreateTaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_task.html',{
                'form': CreateTaskForm,
                'error':'Please provide valida data.'
            })
@login_required       
def task_detail(request, task_id):
    if request.method == 'GET':
        task_detail = get_object_or_404(Tasks, pk=task_id, user=request.user)
        form = CreateTaskForm(instance=task_detail)
        return render(request,'task_detail.html',{
            'task_detail':task_detail,
            'form':form
        })
    else:
        try: 
            task_detail = get_object_or_404(Tasks, pk=task_id, user=request.user)
            form = CreateTaskForm(request.POST, instance=task_detail)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'task_detail.html',{
            'task_detail':task_detail,
            'form':form,
            'error':'Error updating task.'
        })
@login_required
def complete_task(request, task_id):
    task_detail = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':
        task_detail.datecomplete = timezone.now()
        task_detail.save()
        return redirect('tasks')
@login_required   
def delete_task(request, task_id):
    task_detail = get_object_or_404(Tasks, pk=task_id, user=request.user)
    if request.method == 'POST':
        task_detail.delete()
        return redirect('tasks')