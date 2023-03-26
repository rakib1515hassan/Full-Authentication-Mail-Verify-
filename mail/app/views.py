from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import random
import time

# From User-------------------------------------------------------------------
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# For Email Section------------------------------------------------------------
import uuid
from .utils import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage

from passlib.hash import django_pbkdf2_sha256
# Create your views here.
def base(request):
    pass
def home(request):
    return render(request, "home.html")

def Registration(request):
    if request.method=="POST":
        First_Name = request.POST["first_name"]
        Last_Name = request.POST["last_name"]
        User_Name = request.POST["user_name"]
        Email_Address = request.POST["email"]
        password = request.POST["password"]
        Confirm_Password = request.POST["c_password"]
        if password==Confirm_Password:
            if User.objects.filter(username=User_Name).exists():
                messages.error(request, 'User name is already taken.')
                return redirect(Registration)
            elif User.objects.filter(email=Email_Address).exists():
                messages.error(request, 'Email is already taken.')
                return redirect(Registration)
            else:
                user_obj=User.objects.create(first_name=First_Name , last_name=Last_Name , username=User_Name , email=Email_Address , password=password)
                user_obj.set_password(password)
                user_obj.save()
                messages.warning(request, 'Please check in your email, and verify your account.')
                return redirect(Login)
    return render(request, "Auth/sign-up.html")


# Verify Email-----------------------------------------------------
def activate_email(request, email_token):
    try:
        obj= Profile.objects.filter(email_token = email_token).first()
        if obj:
            obj.is_email_verified = True
            obj.save()
            messages.success(request, 'Profile is verified.')
            return redirect('Login')
        else:
            return HttpResponseRedirect("Profile is not valide.")
    except Exception as e:
        messages.error(request, 'Invalid Your Email.')
        return render(request, "Auth/sign-up.html")



def Login(request):
    if request.method=="POST":
        user_name=request.POST["username"]
        passw=request.POST["password"]

        user_obj = User.objects.filter(username=user_name).first()
        if user_obj is None:
            messages.error(request, "User Not Found")
            return redirect('Login')

        pro_obj = Profile.objects.filter(user=user_obj).first()
        if not pro_obj.is_email_verified:
            messages.error(request, "Email Is Not Verified")
            return redirect('Login')

        user=authenticate(username=user_name, password=passw)
        if user is None:
            messages.error(request, "User Not Found")
            return redirect(home)
        login(request, user)
        return redirect('UserProfile')
    return render(request, "Auth/login.html")



@login_required
def LogOut(request):
    auth.logout(request)
    return redirect(Login)


@login_required
def Cv_View(request):
    return render(request, "Auth/Cv_View.html")



@login_required
def UserProfile(request):
    user1= Profile.objects.get(user=request.user)
    return render(request, "Auth/New_Profile.html", locals())


def forget_password(request):
    #otp = random.randint(1111, 9999)
    otp = int(time.strftime("%H%S%M")) + int(time.strftime("%S"))
    if request.method == "POST":
        email = request.POST.get('email')
        user_obj = User.objects.filter(email=email).first()
        pro_obj = Profile.objects.filter(user=user_obj).first()
        if user_obj:
            pro_obj.otp = otp
            pro_obj.save()
            send_otp(email, otp)
            request.session['email'] = request.POST['email']
            messages.success(request, "You OTP is send on your Email. Please Check Out.")
            return redirect('Enter_otp')
        else:
            messages.error(request, "Invalid Email, Please Enter Correct Email.")
    return render(request, "Auth/ForgetPass/forget_password.html")



def Enter_otp(request):
    email = request.session['email']
    if request.session.has_key('email'):
        user_obj = User.objects.filter(email=email).first()
        pro_obj = Profile.objects.filter(user=user_obj).first()
        if request.method == "POST":
            otp_u = request.POST.get('otp')

            if not otp_u:
                messages.error(request, "OTP is Required.")
                return redirect('Enter_otp')
            elif int(pro_obj.otp) == int(otp_u):
                messages.success(request, "Set New Password.")
                return redirect('password_reset')
            else:
                messages.error(request, "OTP is Invalid.")
                return redirect('Enter_otp')
    else:
        return redirect('forget_password')
    return render(request, "Auth/ForgetPass/enter_otp.html")



def password_reset(request):
    if request.session.has_key('email'):
        email = request.session['email']
        password = request.POST.get("password")
        user = User.objects.filter(email=email).first()
        if request.method == "POST":
            con_password = request.POST.get("con_password")
            if not password:
                messages.error(request, "Enter New Password.")
            elif not con_password:
                messages.error(request, "Enter Confirm Password.")
            elif django_pbkdf2_sha256.verify(password,user.password):
                messages.error(request, "This Password Already Exists, Try New Password.")
            elif password==con_password:
                user.password = password
                user.set_password(password)
                user.save()
                messages.success(request, 'Successfully set you password.')
                return redirect('Login')
            else:
                messages.error(request, "Password and Confirm Password is not same.")
    return render(request, "Auth/ForgetPass/password_reset.html")



def test(request):
    return render(request, "test.html")