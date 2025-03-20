from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import LoginForm, RegisterForm
from datetime import datetime
from .models import Exercise



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def index_view(request):
    context = {
        'today_date': datetime.today().strftime('%B %d, %Y')
    }
    return render(request, 'index.html', context)

def profile_view(request):
    return render(request, 'profile.html')

@login_required
def workouts_view(request):
    query = request.GET.get('q', '')
    if query:
        exercises_list = Exercise.objects.filter(name__icontains=query)
    else:
        exercises_list = Exercise.objects.all()

    paginator = Paginator(exercises_list, 9)

    page_number = request.GET.get('page')
    exercises = paginator.get_page(page_number)
    return render(request, 'workouts.html', {'exercises': exercises, 'query': query})
