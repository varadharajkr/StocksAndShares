# from .models import Registeration
import imp
import re
from contextlib import redirect_stderr
from http.client import HTTPResponse

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from authentication.models import Registeration


def isValid(s):
     
    # 1) Begins with 0 or 91
    # 2) Then contains 6,7 or 8 or 9.
    # 3) Then contains 9 digits
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(s)


# Create your views here.
def home(request):
    print("inside home function")
    return render(request,"authentication/index.html")


# @csrf_protect
@csrf_exempt
def signup(request):

    fname=request.POST.get('fname')
    lname=request.POST.get('lname')
    dob=request.POST.get('dob')
    username=request.POST.get('email')
    email=request.POST.get('email')
    pass1=request.POST.get('pass1')
    pass2=request.POST.get('pass2')
    phone=request.POST.get('phone')

    if Registeration.objects.filter(username=request.POST.get('email')).exists():
        return JsonResponse({'status': False,'message':'email '+str(username)+' already exist\n hence unable to create account'})
    elif pass1 != pass2:
        return JsonResponse({'status': False,'message':'password1 '+str(pass1)+' and password2 '+str(pass2)+' is not same\n hence unable to create account'})
    elif (isValid(str(phone))):
        return JsonResponse({'status': False,'message':'phone number '+str(phone)+' not valid\n hence unable to create account'})
    elif request.method=="POST" and len(request.POST) != 0:
        print("inside else loop req met POST")
        myuser=Registeration.objects.create(fname=fname,lname=lname,dob=dob,username=username,email=email,pass1=pass1,pass2=pass2,phone=phone) 
        myuser.fname=fname
        myuser.lname=lname
        myuser.dob=dob
        myuser.username=username
        myuser.email=email
        myuser.pass1=pass1
        myuser.pass2=pass2
        myuser.phone=phone

        myuser.save()

        messages.success(request, "Your Account has been succesfully created.")

        # return redirect(request,'authentication/index.html')
        return redirect('/')


# @csrf_protect
@csrf_exempt
def signup_template(request):
    return render(request,"authentication/signup.html")


@csrf_exempt
def signin_template(request):
    return render(request,"authentication/signin.html")


@csrf_exempt
def dashboard(request):
    return render(request,"authentication/dashboard.html")


@csrf_exempt
def signin(request):
    print("inside signin function")
    username_val=str(request.POST.get('username'))
    password_val=str(request.POST.get('password')) 
    print("username and password values are")
    print(username_val)
    print(password_val)
    print(str(username_val.split("@")[0])) 
    if Registeration.objects.filter(username=username_val,pass1=password_val).exists():
        print(username_val +" and "+password_val+" is matching and logged in succesfully")
        # return render('dashboard',username=str(username_val.split("@")[0]))
        return render(request,"authentication/dashboard.html")

@csrf_exempt
def forgotpassword_template(request):
    print("inside forgot password")
    return render(request,'authentication/forgotpassword.html')

@csrf_exempt
def forgotpassword(request):
    print("inside forgot password")
    if Registeration.objects.filter(username=request.POST.get('username')).exists():
        return JsonResponse({'status': True,"message":"user name validated"})
    else:return JsonResponse({'status': False,"message":"user name not registered,\n please register"})

@csrf_exempt
def resetpassword(request):
    print("inside reset password")
    # usr_nm_tbl = Registeration.objects.get(username=str(request.POST.get('username')))
    # usr_nm_tbl.pass1 = str(request.POST.get('pass1'))
    # usr_nm_tbl.pass2 = str(request.POST.get('pass2'))
    # usr_nm_tbl.save()
    try:
        pass1=str(request.POST.get('pass1'))
        pass2=str(request.POST.get('pass2'))
        Registeration.objects.filter(username=str(request.POST.get('username'))).update(pass1=pass1,pass2=pass2)
    except Exception as e:
        print("exception is "+str(e))