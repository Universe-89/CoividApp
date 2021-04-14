from django.shortcuts import render, redirect,HttpResponseRedirect
from register.forms import RegistrationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import urls, logout
import random
from django.core.mail import send_mail
from register.models import Account
from validate_email import validate_email
import time
from variables import variables
from fcm_django.models import FCMDevice
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from django_email_verification import sendConfirm
# Create your views here.

def registration_view(response):
    if response.method == "POST":
        form = RegistrationForm(response.POST)
        if form.is_valid():
            em = form.cleaned_data['email']        
            form.save()
            user = Account.objects.get(email = em)
            user.is_active = True
            user.save()
            #genrateOTP(em)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(response,"register/register.html",{"form":form})


def logout_view(response):
    logout(response)
    return redirect('/')



'''otpStore= []
def genrateOTP(mail):
    otpStore.append(mail)
    randomOTP = random.randint(1000,9999)
    stringOTP = str(randomOTP)
    otpStore.append(stringOTP)
    send_mail("confirm","your otp is"+stringOTP,variables.email,[otpStore[0]],fail_silently=False)
    oldtime = int(time.time())
    otpStore.append(oldtime)

def otp_view(response):
    if(len(otpStore) == 0)  :
        form = RegistrationForm(response.POST)
        return render(response,"register/register.html",{"form":form})
    user = Account.objects.get(email = otpStore[0])
    if response.method=='POST':
        if response.POST.get("cancel") == "cancel":
            user.delete()
            return redirect("/")
        elif response.POST.get("resend")=="resend":
            send_mail("confirm","your otp is "+otpStore[1],variables.email,[otpStore[0]],fail_silently=False)
            otpStore[-1] = int(time.time())
            return render(response,'registration/otpvalidation.html', {'message':"OTP send to your mail"})
        elif response.POST.get("save")=="save":
            randomOTP = response.POST.get("otp")
            newtime = int(time.time())
            if (newtime-otpStore[2])<300:
                if otpStore[1]==randomOTP:
                    user.is_active = True
                    user.save()
                    return redirect("/")
                else:   
                    return render(response,'registration/otpvalidation.html', {'message':"Enter correct OTP"})
            else:
                user.delete()
                return redirect("/")
    else:
        return render(response,'registration/otpvalidation.html', {'message':"OTP send to your mail"}) '''
