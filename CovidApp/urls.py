"""CovidApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from register import views as v
from locations import views as search
from django.contrib.auth import views as auth_views
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter
#from django_email_verification import urls as mail_urls

router = DefaultRouter()

router.register(r'devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',v.registration_view,name = "register"),
    path('logout/',v.logout_view, name='logout'),
    path('location/',search.location , name = 'findDoctors'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='register/password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='register/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='register/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="register/password_reset_complete.html"),name='password_reset_complete'),
    path('otpvalidation/',v.otp_view,name='otpvalidation'),
    path('',include('dailytracker.urls')),
    path('',include('locations.urls')),
    path('',auth_views.LoginView.as_view(template_name="registration/login.html"),name='login'),
    url(r'^', include(router.urls)),
]
# urls.py



'''
ye saare already available forms hai ,agar #path('',include("django.contrib.auth.urls")),isko use karke saare import ho jaate hai customise nahi hote fir to alag alag path de diya
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
password_reset_form.html is that form where we enter email id to get the password reset link
password_reset_done.html is that page where user will be told about that server has sent the link to reset password successfully
password_reset_confirm.html is that form which opens when the reset link is clicked where user will provide new password
password_reset_complete.html a page where user is told that his/her pw is sucessfully changed and can login now with new password
'''