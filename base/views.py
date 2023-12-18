from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm


def home(request):
	context = {}
	return render(request, 'home.html', context)


def login_user(request):
	# Redirecto to home if user is authenticated
	if request.user.is_authenticated:
		return redirect('home')
	
	# Login / authentication
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user =  authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, 'User logged in successfully.')
			return redirect('home')
		else:
			messages.success(request, 'Invalid username/password, try again.')
			return redirect('login')
	
	# Returning 'login.html' if method is GET
	context = {}
	return render(request, 'login.html', context)


def register_user(request):
	# Redirecto to home if user is authenticated
	if request.user.is_authenticated:
		return redirect('home')
	
	# Registering and validation when the method is POST
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password1'])
			login(request, user)
			messages.success(request, 'User Created Successfully.')
			return redirect('home')
	# Returning 'register.html' if method is GET
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form': form})
	
	return render(request, 'register.html', {'form': form})

	
	



def logout_user(request):
	logout(request)
	messages.success(request, 'User logged out successfully.')
	return redirect('home')

