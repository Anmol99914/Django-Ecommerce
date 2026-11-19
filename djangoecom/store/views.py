from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignUpForm,UpdateUserForm,UserInfoForm
from django import forms
from django.db.models import Q


# Create your views here.
def home(request):
    products = Product.objects.all()
    # products = Product.objects.filter(category='2')
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
            messages.success(request,("Username created! Fill the form to provide additional info.."))
            return redirect('update_info')
        else:
            messages.error(request, "Please correct the errors in the form.")
            # messages.success(request,("OOPs! Some error occurred. Please try again!"))
            return render(request, 'register.html',{'form': form})
    else:
        return render(request, 'register.html',{'form': form})

def product(request,pk): 
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product': product})

def category(request, cat):
    # replace hyphen with a space
    cat = cat.replace('-',' ')
    try:
        category = Category.objects.get(name=cat)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html',{'products': products , 'category': category})
    except:
        messages.success(request,("This category doesnot exist!!"))
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',{'categories': categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request, "User has been updated")
            return redirect('home')
        return render(request, 'update_user.html',{'user_form': user_form})
    else:
        messages.success(request,"You must be logged in to access that page!!!!")
        return redirect('home')

def update_info(request):
	if request.user.is_authenticated:
		# Get Current User
		current_user = Profile.objects.get(user__id=request.user.id)
		
		# Get original User Form
		form = UserInfoForm(request.POST or None, instance=current_user)
		if form.is_valid():
			# Save original form
			form.save()

			messages.success(request, "Your Info Has Been Updated!!")
			return redirect('home')
		return render(request, "update_info.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')

def search(request):
    # determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched'] # name from the form

        # query the products db model
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched)) # i means insensitive so Python and python is same

        # test for  null
        if not searched:
            messages.error(request, "That product doesnot exist!!")
            return render(request,'search.html',{})
        else:
            return render(request, "search.html", {'searched':searched})

    return render(request, "search.html", {})
