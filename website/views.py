"""
This module imports several utility functions for handling common HTTP tasks and authentication 
procedures in a Django application.

- The render function from django.shortcuts simplifies the generation of an HttpResponse
  object with a rendered text template, commonly used to return HTML content.
- The redirect function is used to direct a user to a different URL after an action, like
  submitting a form or logging in.

From django.contrib.auth, the following authentication functions are imported:
- authenticate assists in verifying user credentials.
- login commences a user session after successful authentication.
- logout ends a user session, effectively logging the user out.

The messages framework from django.contrib is also imported to enable the creation and
display of temporary messages to the end user, often used for displaying alerts or success messages
after form submissions or actions requiring feedback.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()

    """Method checks whether user logged in..."""
        # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
                # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            # messages.MessageFailure(request, "There Was An Error Logging In, Pleas Try Again...")
            messages.success(request, "There Was An Error Logging In, Pleas Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

# def login_user(request):
# 	pass

def logout_user(request):
    """Logging out user"""
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered! Welcome on board!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be logged in to view that page!")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that...")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')    
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        return redirect('home')
        

    return 