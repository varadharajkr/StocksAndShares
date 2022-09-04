from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "authentication"

urlpatterns = [
    path('',views.home,name="home"),
    path('home',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signup_template',views.signup_template,name="signup_template"),
    path('signin',views.signin,name="signin"),
    path('signin_template',views.signin_template,name="signin_template"),
    path('dashboard',views.dashboard,name="dashboard"),
    # path('signout',views.signout,name="signout"),
    path('forgotpassword',views.forgotpassword,name="forgotpassword"),
    path('forgotpassword_template',views.forgotpassword_template,name="forgotpassword_template"),
]
