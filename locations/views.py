from django.shortcuts import render
import googlemaps
import json
import time
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from django.core.mail import send_mail  
from dailytracker.models import EmergencyContacts
from variables import variables
from pyfcm import FCMNotification
from fcm_django.models import FCMDevice

API_KEY = "AIzaSyCrK-MmntrS_XuIPtjAXNwKchjdaceVkYw"
longitude_orign = 0  
latitude_orign  = 0
latitude_desti  = 0 
longitude_desti = 0

# Create your views here.
def location (response):
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
            cache.add('latitude_desti',latitude_desti)
            cache.add('longitude_desti',longitude_desti)
            driverLocation = requests.get('http://localhost:8000/ambulance/view/' + latitude_orign + '/' + longitude_orign + '/',params=response.GET)
            driver = driverLocation.json()

            # /sendNotification(hospitalName)

            contactlist = EmergencyContacts.objects.filter(user=response.user)
            for contact in contactlist:
                send_mail("Emergency Alert","Due to serious condition "+ response.user.name +" is taken to "+ hospitalName + " hospital <br> hospital address :- " +  hospitalAdd + " is taken by " + driver['driverName'] + "  Ambulance Number :- " + driver['driverAmbulance'] + "ContactNo. :- "+ driver['driverContact'],variables.email,[contact.contact])

            mapInfo = {"hospitalName":hospitalName,"hospitalAdd":hospitalAdd,"driverName":driver['driverName'],"driverAmbulance":driver['driverAmbulance'],"latiOrigin":latitude_orign,"lngiOrigin":longitude_orign,"latiDesti":latitude_desti,"lngiDesti":longitude_desti,"latDriver":driver['latitude'],"lngDriver":driver['longitude']}
            return render(response,"locations/map.html",mapInfo)
        else:
            return render(response,"dailytracker/home.html",{})
    else:
        return render(response,"locations/start.html",{})
    
# def sendNotification (hospital_name) : 
    
#     push_service = FCMNotification(api_key="BDx-hNlhd6L8KMnxem3-RyuxWg41zvlK-cEPWmFHseteXzhpOoDLk7l0pWX3zBl0K0cR2qihEQ9bnLmIPr_7Dis")
#     registration_id = "1"
#     message_title = "Emergency"
#     message_body = "Need to take a patient to" + hospital_name
#     result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
#     print (result)

class currentLocation(APIView):
    def get(self, response):
        # return Response({'origin' :{'lng':cache.get('longitude_orign'),'lat':cache.get('latitude_orign')},
        #                 'distination':{'lng':cache.get('longitude_desti'),'lat':cache.get('latitude_desti')}})
        return {}

    def post(self, response):
        pass

        
# def room(request, room_name):
#         mapInfo = {"hospitalName":hospitalName,"hospitalAdd":hospitalAdd,"driverName":driver['driverName'],"driverAmbulance":driver['driverAmbulance'],"latiOrigin":latitude_orign,"lngiOrigin":longitude_orign,"latiDesti":latitude_desti,"lngiDesti":longitude_desti,"latDriver":driver['latitude'],"lngDriver":driver['longitude'],'room_name': room_name}
#         return render(request, 'locations/map.html', mapInfo)