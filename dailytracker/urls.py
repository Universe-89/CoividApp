from django.urls import path
from . import views

urlpatterns = [
path('dailytracker/',views.tracker, name="dailytracker"),
path('emergencycontacts/',views.emergencycontacts,name='emergencycontacts'),
path('home/',views.home, name="home"),
path('health/',views.health,name="health"),
path('sos/', views.sos,name='sos'),
path('addition/',views.add,name='add')
]