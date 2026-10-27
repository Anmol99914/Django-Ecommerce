from django.shortcuts import render,redirect
from .models import Product
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms



# Create your views here.
def home(request):
    # products = Product.objects.all()
    products = Product.objects.filter(category='2')
    return render(request, 'home.html',{'products': products})

def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request,("Invalid credentials"))
            return redirect('login')
    else:
        return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been logged out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # login user
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request,("You have registered successfully!"))
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors in the form.")
            # messages.success(request,("OOPs! Some error occurred. Please try again!"))
            return render(request, 'register.html',{'form': form})
    else:
        return render(request, 'register.html',{'form': form})

def product(request,pk): 
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product': product})
