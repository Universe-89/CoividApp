from django.urls import path
from . import views

urlpatterns = [
    path('getLocation/',views.currentLocation.as_view(), name="getCurrentLocation"),
    path('qrcode/',views.qrcode, name="getCurrentLocation"),
    path('<str:room_name>/', views.location, name='location'),
]