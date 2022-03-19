from django.shortcuts import render,redirect
from .models import Users
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login

import correction_detection

# Create your views here.

def index(request):
    return render(request, "correction_detection/index.html")

def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        print(form)
        if form.is_valid():
            print("valid form")
            form.save()
            print("form saved")
            username = form.cleaned_data.get('username')
            messages.success(request,f'account created for {username}')
            return redirect('login')
        else:
            print("invalid form")

    form = CreateUserForm()
    context = {"form":form, "title":"Register"}
    return render(request, "correction_detection/register.html", context)



def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('portfolio')
        else:
            messages.info(request, "email or password is incorrect")

    return render(request, "correction_detection/login.html")


def portfolio(request):
    return render(request, 'correction_detection/portfolio.html',{"title":"Portfolio"})