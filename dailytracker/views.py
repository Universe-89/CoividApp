from django.shortcuts import render, redirect,HttpResponseRedirect
from django.http import HttpResponseRedirect
from .models import BasicInfo,EmergencyContacts
from register.models import Account
from django.contrib import messages
from .models import BasicInfo
from .models import HealthInfo
from django.core.mail import send_mail  
from variables import variables
import googlemaps
import json
import time
import requests

API_KEY = "AIzaSyCrK-MmntrS_XuIPtjAXNwKchjdaceVkYw"

def home(response):
    if(response.method == "POST"):
        if(response.POST.get('save')):
            gmaps = googlemaps.Client(key = API_KEY)
            longitude_orign = response.POST.get('lon')
            latitude_orign = response.POST.get('lat')
            # adding to cache 
            # cache.add('longitude_orign',longitude_orign)
            # cache.add('latitude_orign',latitude_orign)
            
            position = str(latitude_orign) + ","+ str(longitude_orign)
            places_result  = gmaps.places_nearby(location=position, radius = 2000,open_now = False , type = 'hospital')
            time.sleep(2)
            stored_results = []
            for place in places_result['results']:

                # define the place id, needed to get place details. Formatted as a string.
                my_place_id = place['place_id']

                # define the fields you would liked return. Formatted as a list.
                my_fields = ['name','geometry','formatted_address']

                # make a request for the details.
                places_details  = gmaps.place(place_id= my_place_id , fields= my_fields)

                # print the results of the details, returned as a dictionary.
                # print(places_details['result'])

                # store the results in a list object.
                stored_results.append(places_details['result'])

                break

            latitude_desti  = stored_results[0]['geometry']['location']['lat']
            longitude_desti = stored_results[0]['geometry']['location']['lng']
            hospitalName    = stored_results[0]['name']
            hospitalAdd     = stored_results[0]['formatted_address']
            driverLocation = requests.get('http://localhost:8000/ambulance/view/' + latitude_orign + '/' + longitude_orign + '/',params=response.GET)
            driver = driverLocation.json()

            # /sendNotification(hospitalName)

            contactlist = EmergencyContacts.objects.filter(user=response.user)
            for contact in contactlist:
                send_mail("Emergency Alert","Due to serious health condition "+ response.user.name +" is taken to "+ hospitalName + " Hospital \nHospital Address :- " +  hospitalAdd + "\n Driver Name : " + driver['driverName'] + "  \nAmbulance Number :- " + driver['driverAmbulance'],variables.email,[contact.contact])

            mapInfo = {"hospitalName":hospitalName,"hospitalAdd":hospitalAdd,"driverName":driver['driverName'],"driverAmbulance":driver['driverAmbulance'],"latiOrigin":latitude_orign,"lngiOrigin":longitude_orign,"latiDesti":latitude_desti,"lngiDesti":longitude_desti,"latDriver":driver['latitude'],"lngDriver":driver['longitude']}
            return render(response,"locations/map.html",mapInfo)
        else:
            return render(response,"dailytracker/home.html",{})

    return render(response,"dailytracker/home.html",{})

def health(response):
    if(response.method == "POST"):
        if(response.POST.get("save") == "save"):
            info1                           = HealthInfo()
            info1.diabetic                  = answer(response.POST.get("diabetic-radio"))
            info1.cancer_patient            = answer(response.POST.get("cancer-radio"))
            info1.cardiac_patient           = answer(response.POST.get("cardiac-radio"))
            info1.asthama_patient           = answer(response.POST.get("asthama-radio"))
            info1.blood_pressure_patient    = answer(response.POST.get("bp-radio"))
            info1.weak_immunity             = answer(response.POST.get("immunity-radio"))
            info1.other                     = response.POST.get("other")
            info1.save()
            response.user.healthinfo.add(info1)
            return render(response,"dailytracker/home.html",{})
    return render(response,"dailytracker/health.html",{})

def tracker(response):
    if(response.method == "POST"):
        if(response.POST.get("save") == "save"):
            info                      = BasicInfo()
            info.temp                 = response.POST.get("temperature")
            info.oxygen_level         = response.POST.get("oxygen-level")
            info.headache             = answer(response.POST.get("headache-radio"))
            info.running_nose         = answer(response.POST.get("running-nose-radio"))
            info.sore_throat          = answer(response.POST.get("sore-throat-radio"))
            info.loss_smell_taste     = answer(response.POST.get("loss-smell-taste-radio"))
            info.difficulty_breathing = answer(response.POST.get("difficulty-breathing-radio"))
            info.travel               = response.POST.get("travel")
            info.save()
            response.user.basicinfo.add(info)

            return render(response,"dailytracker/home.html",{})

    return render(response,"dailytracker/tracker.html",{})


def answer(str):
    if(str == 'yes'):
        return True
    return False

def update(response,contactmail):
    uname=response.user.email
    currentuser = response.user
    newcontact = EmergencyContacts.objects.get(user=currentuser,contact=contactmail)
    newcontact.contact = response.POST.get("email")
    newcontact.phone = response.POST.get("phone")
    newcontact.name = response.POST.get("name")
    newcontact.save()
    send_mail("Emergency Contact","hello there, You are being added as Emergency Contact of "+uname,variables.email,[newcontact.contact])


def emergencycontacts(response):
    if response.method=="POST":
        if(response.POST.get("update1")):
            contactmail = response.POST.get('update1')
            update(response,contactmail)
            return redirect('/emergencycontacts')

        if(response.POST.get("update11")):
            contactmail=response.POST.get('update11')
            update(response,contactmail) 
            return redirect('/emergencycontacts')


        if(response.POST.get("update2")):
            contactmail = response.POST.get('update2')
            update(response, contactmail)            
            return redirect('/emergencycontacts')
        
        if(response.POST.get("delete1")):
            contactmail=response.POST.get('delete1')
            EmergencyContacts.objects.get(user=response.user, contact=contactmail).delete()
            return redirect('/emergencycontacts')

        if(response.POST.get("delete11")):
            contactmail=response.POST.get('delete11')
            EmergencyContacts.objects.get(user=response.user, contact=contactmail).delete()
            return redirect('/emergencycontacts')

        if(response.POST.get("delete2")):
            contactmail=response.POST.get('delete2')
            EmergencyContacts.objects.get(user=response.user, contact=contactmail).delete()
            return redirect('/emergencycontacts')

    else:
        contacts = response.user
        contactlist = EmergencyContacts.objects.filter(user=contacts)
        length = len(contactlist)
        if length==2:
            contact1 = contactlist[0]
            contact2 = contactlist[1]
            return render(response,'dailytracker/showcontacts.html',{"contactlist":contactlist,"c1":contact1,"c2":contact2})
        if length==1:
            return render(response,'dailytracker/showcontacts.html',{"contactlist":contactlist,"c1":contactlist[0]})
        else:
            return render(response,'dailytracker/showcontacts.html',{"contactlist":contactlist})        

def add(response):
    uname = response.user.email
    if response.method=="POST":
        if response.POST.get("save")=="save":
            newcontact = EmergencyContacts()
            newcontact.contact = response.POST.get("emailcontact")
            newcontact.phone = response.POST.get("phone")
            newcontact.name = response.POST.get("name")
            newcontact.save()
            send_mail("Emergency Contact","hello there, You are being added as Emergency Contact of "+uname,variables.email,[newcontact.contact])
            response.user.emergencycontacts.add(newcontact)
            return redirect('/emergencycontacts')
    else:
        return render(response,"dailytracker/emergencycontacts.html",{})
        

        
def sos(response):
    contacts = response.user
    contactlist = EmergencyContacts.objects.filter(user=contacts)
    if(len(contactlist)==2):
        recieverEmail1 = contactlist[0].contact
        recieverEmail2 = contactlist[1].contact
        send_mail("Emergency Situation!!","Situation of " + contacts.name + " does't seems right he/she might need your help" ,variables.email,[recieverEmail1,recieverEmail2],fail_silently=False)
        return render(response,"dailytracker/home.html",{})
    if(len(contactlist)==1):
        recieverEmail1 = contactlist[0].contact
        send_mail("Emergency Situation!!","Situation of " + contacts.name + " does't seems right he/she might need your help" ,variables.email,[recieverEmail1],fail_silently=False)
        return render(response,"dailytracker/home.html",{})

    else:
        messages.info(response, 'you have not added your emergency contacts')
        return render(response, "dailytracker/home.html",{})

