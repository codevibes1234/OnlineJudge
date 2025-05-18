from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from accounts.models import OTP,ExtendedUser
import math
import random
import smtplib

# Create your views here.
def verifyEmail(request,otpId,uId):
    next_url = request.GET.get('next') or request.POST.get('next')
    user = User.objects.get(id=uId)
    generatedOTP = OTP.objects.get(id=otpId)
    if request.method == "POST":
        otp = request.POST.get('otp')
        if otp == generatedOTP.otp:
            messages.success(request,'OTP verified')
            login(request,user)
            generatedOTP.delete()
            return redirect(next_url)
        else:
            messages.error(request,'Incorrect OTP')
            user.delete()  
            generatedOTP.delete()          
            return redirect('/accounts/login/?next='+str(next_url))

    return render(request,'verify.html',{'next': next_url})

def register(request):
    next_url = request.GET.get('next','') or request.POST.get('next','')
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if request.user.is_authenticated:
            messages.error(request,'You are already logged in, please logout before logging in')
            return redirect(f'/user/{request.user.id}/')
        
        if uname in User.objects.values_list('username',flat = True):
            messages.error(request,'User already exists')
            return render(request,'register.html',{'next':next_url})
        
        if email in User.objects.values_list('email',flat = True):
            messages.error(request,'This email already exists')
            return render(request,'register.html',{'next':next_url})
        
        user = User.objects.create_user(username=uname,email=email)
        user.set_password(password)
        user.save()
        exUser = ExtendedUser.objects.create(user=user,solvedProblems="")
        exUser.save()
        digits="0123456789"
        generatedOTP=""
        for i in range(6):
            generatedOTP+=digits[math.floor(random.random()*10)]
        otpObj = OTP(otp=generatedOTP)
        otpObj.save()
        msg = generatedOTP + " is your OTP"
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("xyz@gmail.com", "---- ---- ---- ----")
        s.sendmail('xyz@gmail.com',email,msg)
        if next_url == '':
            next_url = '/problems'
        return redirect(f'/accounts/verify/{otpObj.id}/{user.id}/?next='+str(next_url))
    
    if next_url == '':
        next_url = '/problems'
    return render(request,'register.html',{'next': next_url})
        
def login_user(request):
    next_url = request.GET.get('next','') or request.POST.get('next','')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if request.user.is_authenticated:
            messages.error(request,'You are already logged in, please logout before logging in')
            return redirect(f'/user/{request.user.id}/')
    
        if not User.objects.filter(username=username).exists():
            messages.error(request,'User with this username does not exist')
            return render(request,'login.html',{'next':next_url})
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request,'Invalid password')
            return render(request,'login.html',{'next':next_url})
        
        login(request,user)
        messages.success(request,'Login successful!')
        if next_url == '':
            next_url = '/problems'
        return redirect(next_url)
    
    if next_url == '':
        next_url = '/problems'
    return render(request, 'login.html', {'next': next_url})

def logout_user(request):
    logout(request)
    messages.success(request,'User logged out successfully')
    return redirect('/problems')