from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import blogpost

class signupForm(UserCreationForm):
    password1 = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control','id':'password1','placeholder':'Password'}),label="Password")
    password2 = forms.CharField(min_length=8,max_length=20,widget=forms.PasswordInput(attrs={'class':'form-control','id':'password2','placeholder':'Confirm Password'}),label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username','id':'username'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email','id':'email'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name','id':'first_name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name','id':'last_name'})
        }
        


class SigninForm(AuthenticationForm):
    # Define a 'username' field with a maximum length of 60 characters,
    # and specify widget attributes for rendering in HTML.
    username = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    
    # Define a 'password' field, and specify widget attributes for rendering in HTML.
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    
class blogForm(forms.ModelForm):
    class Meta:
        model = blogpost
        fields = ['title','des']
        labels = {'title':'Title','des':'Description'}
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'des' : forms.Textarea(attrs={'class':'form-control','placeholder':'Description'})
        }