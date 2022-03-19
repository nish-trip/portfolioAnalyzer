from django.shortcuts import render,redirect
from .models import Users
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

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
    # if request.method == "POST":
    #     mail_id = request.POST['email']
    #     passwd = request.POST['password']
    #     confirmed_password = request.POST['confirmed_password']
    #     if passwd != confirmed_password:
    #         print("the passwords do not match")
    #         return render(request, 'correction_detection/register.html')

    #     print("registered new user")
    #     user = Users(email=mail_id, password=passwd)
    #     user.save()
    #     return redirect('portfolio')
    #     # redirect to portfolio page, localhost:8000/postfolio, which has the list of stocks 

    # return render(request, 'correction_detection/register.html')


def login(request):

    if request.method == "POST":
        print(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email = email, password = password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('portfolio')
        else:
            messages.info(request, "email or password is incorrect")

    return render(request, "correction_detection/login.html")
    # if request.method == "POST":
    #     mail_id = request.POST['email']
    #     passwd = request.POST['password']

    #     queryset = Users.objects.all()
    #     if queryset.filter(email = mail_id).exists():
    #         record = queryset.filter(email = mail_id).values()[0]
    #         if record["password"] != passwd:
    #             print("invalid password")
    #             return redirect('login')
            
    #         else:
    #             print("successfully logged in")
    #             return redirect('portfolio')
        
    #     else:
    #         print("new user, please register")
    #         return redirect('register')

    
    # if request.method == "GET":
    #     return render(request, 'correction_detection/login.html', {"title":"Login"})


def portfolio(request):
    return render(request, 'correction_detection/portfolio.html',{"title":"Portfolio"})