from django.shortcuts import render ,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
# from django.contrib.auth.decorators import login_required
# Create your views here.

def SignUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created!You can sign in now...')
            login(request,user)
            return redirect('signin')    #requires name in url
    else:
        form = UserCreationForm()
    return render(request,'signup.html',{'form':form})


def SignIn(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request,'signin.html',{'form':form})

# @login_required
def Profile(request):
    name = None
    if request.user.is_authenticated:
        name = request.user.username
    return render(request,'profile.html',{'name':name})