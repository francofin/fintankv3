from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Portfolio
# Create your views here.
def register_user(request):
    if request.method=='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        password_min = 6

        if len(password) < password_min:
            messages.error(request, 'Your Password is Too Short, Please choose a password at least 6 characters long!')
            return redirect('register_user')
        else:
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username Already Exists')
                    return redirect('register_user')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Email Already Exists!')
                        return redirect('register_user')
                    else:
                        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password)
                        auth.login(request, user)
                        messages.success(request, 'you are now logged in')
                        return redirect('dashboard')
                        user.save()
                        messages.succes(request, 'Account Successfully Created. Welcome')
                        return redirect('index')
            else:
                messages.error(request, 'Passwords Do Not Match!')
                return redirect('register_user')
    else:
        return render(request, 'pages/register.html')


def add_to_portfolio(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        ticker = request.POST['ticker']

        portfolio = Portfolio(user_id = user_id, ticker=ticker)
        portfolio.save()
        messages.success(request, str(ticker)+' Has been Successfully Added to Your Portfolio')
        return redirect('/research/')


def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You Are Successfully Logged In! Welcome')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid LogIn Credentials')
            return redirect('login')
    return render(request, 'pages/login.html')

def logout(request):
    if request.method=='POST':
        auth.logout(request)
        return redirect('login')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    user_stocks = Portfolio.objects.all().filter(user_id=request.user.id)
    # user_lifestyle = LifestyleDashboard.object.all().filter(user_id=request.user.id)

    stocks = {
        'user_stocks': user_stocks
    }
    return render(request, 'pages/dashboard.html', stocks)
