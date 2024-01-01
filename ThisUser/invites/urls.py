from django.urls import path
from . import views
urlpatterns =[
    path('signup/',views.SignUp),
    path('signin/',views.SignIn, name='signin'),
    path('profile/',views.Profile, name='profile')
]