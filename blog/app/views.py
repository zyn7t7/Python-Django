from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import signupForm,blogForm,SigninForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import blogpost
from django.contrib.auth.models import User
# from django.contrib.auth.forms input F

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')

def post(request):
    if request.user.is_authenticated:
        get = blogpost.objects.all()
        return render(request,'posts.html',{'get':get})
    else:
        return redirect('/signin/')

@login_required
def profile(request):
    if request.user.is_authenticated:
        email = request.user.email
        user_name = request.user.username
        return render(request,'profile.html',{'name':request.user,'email':email,'username':user_name})
    else:
        return HttpResponseRedirect('/login/')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Your Password Has Successfully updated!')
            return redirect('profile')
        else:
            messages.error(request,'Sorry! Cant Change Password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'change_password.html',{'form':form})

def addpost(request):
    if request.user.is_authenticated:
            if request.method == 'POST':
                form = blogForm(request.POST)
                if form.is_valid():
                    title = form.cleaned_data['title']
                    des = form.cleaned_data['des']
                    CT = blogpost(title =title,des = des)
                    CT.save()
                    return redirect('/posts/')
            else:
                form = blogForm(auto_id=True)
            return render(request,'addpost.html',{'form':form})
    else:
        return redirect('/signin/')
                
def deletePost(request,id):
    db = blogpost.objects.get(pk = id)
    try:
        db.delete()
    except:
        return ('/posts/')
    return redirect('/posts/')  

def updatePost(requst,id):
    row = blogpost.objects.get(pk=id)
    if requst.method == 'POST':
        form = blogForm(requst.POST,instance=row)
        if form.is_valid():
            form.save()
            return redirect('/posts/')
    else:
        form = blogForm(instance=row)
    return render(requst,'addpost.html',{'form':form})
               
def signup(request):
    if request.method == "POST":
        form = signupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"Congratulations Your Account Has Been Created Successfully!") 
            return redirect('/signup/')
        else:
            messages.error(request,"Error creating the account.Please check the form") 
            return redirect('/signup/')      
    else:
        form = signupForm()
    return render(request,'signup.html',{'form':form})


# def signin(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             form = signin(request=request,data=request.POST)
#             if form.is_valid():
#                 username = request.POST["username"]
#                 password = request.POST["password"]
#                 user = authenticate(request, username=username, password=password)
#                 if user is not None:
#                         login(request, user) 
#                         return HttpResponseRedirect('/posts/')
#             else:
#               return HttpResponse("Sorry Invalid")                   
#         else:
#             form = signin(request=request,data=request.GET)
#     else:
#             return redirect('/home/')
#     return render(request,'signin.html',{'form':form})

  # Assuming your form is in the same app

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SigninForm(data=request.POST)  # Use SigninForm instead of signin
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect('/posts/')
                else:
                    messages.error(request,"Enter Username and Password")
            else:
                messages.error(request,"Invalid Username and Password")  # Adjust this according to your needs
        else:
            form = SigninForm()  # Use SigninForm instead of signin
        return render(request, 'signin.html', {'form': form})
    else:
        return redirect('/signin/')

def signout(request):
    logout(request)
    return redirect('/signin/')