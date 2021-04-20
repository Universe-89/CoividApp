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
            genrateOTP(em)
            return redirect('/otpvalidation')
    else:
        form = RegistrationForm()
    return render(response,"register/register.html",{"form":form})


def logout_view(response):
    logout(response)
    return redirect('/')



otpStore = []

def genrateOTP(mail):
    otpStore.append(mail)
    randomOTP = random.randint(1000,9999)
    stringOTP = str(randomOTP)
    otpStore.append(stringOTP)
    send_mail("confirm","your otp is"+stringOTP,variables.email,[otpStore[0]],fail_silently=False)
    oldtime = int(time.time())
    otpStore.append(oldtime)

def otp_view(response):
    if(len(otpStore) == 0):
        return redirect("/")
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
        return render(response,'registration/otpvalidation.html', {'message':"OTP send to your mail"})


# class UserRegister(APIView):
#     def post(self, request):
#         token = Token.objects.create(user=user)
#         json = serializer.data
#         fcm_token = json['fcm_token']
#         user = json['id'] 
#         device = FCMDevice()
#         device.registration_id = fcm_token
#         device.type = "Web"
#         device.name = "Can be anything"
#         device.user = user
#         device.save()
#         return Response(
#             {
#                 "token": token.key,
#                 "error": False
#             },
#             status=status.HTTP_201_CREATED)

# class UserAuth(APIView):
#     def post(self, request):
#         fcm = request.data.get("fcm_token")
#         user = authenticate(email=request.data.get("email"),
#                             password=request.data.get("password"))
#         if user is not None:
#             ser = UserDetailSerializer(user)
#             fb = User.objects.get(id=usser.id)
#             print(ser.data['id'])
#             try:
#                 devices = FCMDevice.objects.get(user=ser.data['id'])
#             except FCMDevice.DoesNotExist:
#                 devices = None
#             if devices is None:
#                 device = FCMDevice()
#                 device.user = user
#                 device.registration_id = fcm
#                 device.type = "Android"
#                 device.name = "Can be anything"
#                 device.save()
#             else:
#                 devices.registration_id = fcm
#                 devices.save()
#             try:
#                 token = Token.objects.get(user_id=user.id)
#             except:
#                 token = Token.objects.create(user=user)
#                 print(token.key)
#                 print(user)

#             return Response({"token": token.key, "error": False})
#         else:
#             data = {
#                 "error": True,
#                 "msg": "User does not exist or password is wrong"
#             }

#             return Response(data, status=status.HTTP_401_UNAUTHORIZED)