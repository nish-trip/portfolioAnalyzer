from urllib import request
from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Stocks

# Create your views here.

def index(request):
    print(f"current user: {request.user.id}\n")
    return render(request, "correction_detection/index.html")

def register(request):
    # is the user is already authenticated then redirect to portfolio
    if request.user.is_authenticated:
        return redirect('portfolio')

    # runs when the form is submitted
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
    # is the user is already authenticated then redirect to portfolio
    print(f"current user: {request.user.id}\n")
    if request.user.is_authenticated:
        return redirect('portfolio')

    # runs when the login form is submitted
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # if user is authenticated then log them in and redirect to portfolio
        if user is not None:
            auth_login(request, user)
            return redirect('portfolio')
        else:
            messages.info(request, "email or password is incorrect")

    return render(request, "correction_detection/login.html")

# logout functionality 
def logout(request):
    auth_logout(request)
    return redirect('login')

# only allowed to visit this place if the user is logged in 
@login_required(login_url='login')
def portfolio(request):
    print(f"current user: {request.user.id}\n")
    if request.method == "POST":
        if "add" in request.POST:
            username = request.user
            context = {"title":"Portfolio", "username":username}
            stock_name = request.POST["name"]
            record = Stocks.objects.filter(name=stock_name, owner_id=request.user.id).values_list().first()
            if record is not None: # if the stock is already present 
                print("Stock has already been addded to the watchlist")

            else:# if the stock with that name is not present then we add it to the database
                stock = Stocks(name=stock_name, owner_id=request.user.id)
                stock.save()  
                print(f"added {stock_name} to your watchlist")
            

        if "remove" in request.POST:
            stock_name = request.POST["remove_stock"]
            try:
                record = Stocks.objects.filter(name=stock_name, owner_id =request.user.id).values()[0]
                record_id = record['id']
                Stocks.objects.filter(id=record_id).delete()
                print(f'deleted {stock_name} from your watchlist')

            except Exception as e:
                print("You do not have this stock in your watclist")
            
    # list of stocks added by the current user
    stocks_list = [s[0] for s in Stocks.objects.filter(owner_id = request.user.id).values_list('name')]
    print(stocks_list)
    username = request.user
    context = {"title":"Portfolio", "username":username} 
    return render(request, 'correction_detection/portfolio.html', context)