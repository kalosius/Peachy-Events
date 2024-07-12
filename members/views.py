from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 

def logout_user(request):
    logout(request)
    messages.success(request, 'You were Logged Out!')
    return redirect('home')



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'There was an error Logging In, Try Again!')
            return redirect('login')


    else:
        return render(request, 'authenticate/login.html', {})

