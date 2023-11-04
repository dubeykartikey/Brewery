from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import LoginForm, SignupForm
from django.contrib.auth import authenticate
# Create your views here.

def home(request):
    return render(request, './auth.html')

def signup(request):
    signin_form = LoginForm()
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('home')
    else:
        signup_form = SignupForm()
    return render(request, './auth.html', {'signup_form': signup_form, 'signin_form': signin_form})

def signin(request):
    form = LoginForm()
    message = ''
    print(form)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            print(user)
            if user is not None:
                login(request, user)
                message = f'Hello {user.username}! You have been logged in'
                return render(request, './home.html')
            else:
                message = 'Login failed!'
    return render(
        request, './auth.html', context={'form': form, 'message': message})