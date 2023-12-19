from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# ----------------- Record Management -----------------
def home(request):
	record = Record.objects.all()
	context = {'records': record}
	return render(request, 'home.html', context)


def view_record(request, pk):
	record = Record.objects.get(id=pk)
	context = {'record': record}
	return render(request, 'view_record.html', context)


def add_record(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = AddRecordForm(request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, 'Record added successfully.')
				return redirect('home')
		else:
			form = AddRecordForm()
			return render(request, 'add_record.html', {'form': form})
	else:
		messages.error(request, 'Please Login to add new record.')
		return redirect('login')

def edit_record(request, pk):
	record = Record.objects.get(id=pk)
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = AddRecordForm(request.POST, instance=record)
			if form.is_valid():
				form.save()
				messages.success(request, 'Record updated successfully')
				return redirect(f'/records/{pk}')
		else:
			form = AddRecordForm(instance=record)
			return render(request, 'edit_record.html', {'form': form})
	else:
		messages.error(request, 'Please login to edit record.')
		return redirect('login')


def delete_record(request, pk):
	if request.user.is_authenticated:
		record = Record.objects.get(id=pk)
		record.delete()
		messages.success(request, 'Record deleted successfully.')
		return redirect('home')
	else:
		messages.error(request, 'Unable to delete, Unauthorized user.')
		return redirect(f'/records/{pk}')
		



# ----------------- User Management -----------------
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

