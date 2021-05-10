import requests, time, threading
import os
from store.models.weatherdata import Weatherdata
from django.shortcuts import render , redirect , HttpResponseRedirect
from datetime import datetime
from django.contrib.sessions.models import Session
from store.models.customer import Customer
from store.models.farmer import Farmer

def weathsms():
    weath = Weatherdata.objects.all()
    test_2 = {'test': weath}

    for i in test_2['test']:

        coordinates = {"lat": i.latitude, "lon": i.longitude}
        #print(coordinates)
        key = ""  #openweathermap key here

        wetherApi = "https://api.openweathermap.org/data/2.5/weather"

        weather = requests.get(wetherApi, params={**coordinates,"appid":key}).json()


        weather_description = weather["weather"][0]["description"]
        temp = weather["main"]["temp"] - 273.15  #float
        wind_speed = weather["wind"]["speed"]    #float
        humidity = weather["main"]["humidity"]   #int




        if temp > 50.0 or wind_speed > 10.0 or humidity > 60:


            test = 'Hello Sir/Madam, the current weather is '+str(weather_description)+' and the temperature is '+str("{:.2f}".format(temp))+' °C.'
        
            url = "https://www.fast2sms.com/dev/bulk"
            payload = "sender_id=FSTSMS&message=Dear farmer, be Alert. The current Weather is "+str(weather_description)+" ,the Temperature is "+str("{:.2f}".format(temp))+" C, the Wind speed is "+str("{:.2f}".format(wind_speed))+" km/hr and the Humidity is "+str(humidity)+" %.&language=english&route=p&numbers="+i.phone+""
            headers = {
            'authorization': "",  #Fast2SMS Authorization key here
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)


while(1):
    weathsms()

def weatherdatas(request):


    ipinfo = requests.get("https://ipapi.co/json").json()
    #coordinates = {"lat": 22.3005, "lon": 73.204}
    coordinates = {"lat": ipinfo["latitude"], "lon": ipinfo["longitude"]}

    key = "f2c5f105d6e526846a31c4898f10480f"

    wetherApi = "https://api.openweathermap.org/data/2.5/weather"

    weather = requests.get(wetherApi, params={**coordinates,"appid":key}).json()


    #threading.Timer(1000*60, showWeather()).start()


    latitude =  ipinfo["latitude"]
    longitude = ipinfo["longitude"]
    #latitude = 22.3005
    #longitude = 73.204
    
    weather_description = weather["weather"][0]["description"]
    weather_main = weather["weather"][0]["main"]
    
    temp = weather["main"]["temp"] - 273.15
    temp_feels_like = weather["main"]["feels_like"] - 273.15
    temp_min = weather["main"]["temp_min"] - 273.15
    temp_max = weather["main"]["temp_max"] - 273.15
    
    pressure = weather["main"]["pressure"]
    humidity = weather["main"]["humidity"]
    visibility = weather["visibility"]
    wind_speed = weather["wind"]["speed"] 
    dire = weather["wind"]["deg"]
    clouds = weather["clouds"]["all"]
    
    country = weather["sys"]["country"]
    
    city = weather["name"]

    day_1 = temp + 1
    day_2 = temp 
    day_3 = temp 
    day_4 = temp + 3
    day_5 = temp + 2
    day_6 = temp + 1
    
    
    #print(weather)

    
    timezone = int(weather['timezone'])
    #print('Timezone : {}'.format(timezone))

    sunrise_utc = int(weather['sys']['sunrise'])
    sunrise_local = datetime.utcfromtimestamp(sunrise_utc + timezone).strftime('%H-%M-%S')
    #print('Sunrise : {}'.format(sunrise_local))

    #print(sunrise_local[:2]+'h '+ sunrise_local[3:5]+'m '+sunrise_local[6:]+'s')
    sunrise = sunrise_local[:2]+'h '+ sunrise_local[3:5]+'m '+sunrise_local[6:]+'s'
    #print(sunrise)


    sunset_utc = int(weather['sys']['sunset'])
    sunset_local = datetime.utcfromtimestamp(sunset_utc + timezone).strftime('%H-%M-%S')
    #print('sunset : {}'.format(sunset_local))
    sunset = sunset_local[:2]+'h '+ sunset_local[3:5]+'m '+sunset_local[6:]+'s'
    #print(sunset)

    current_month_text = datetime.now().strftime('%B')
    current_day_full_text = datetime.now().strftime('%A')
    current_year_full = datetime.now().strftime('%Y') 
    current_day = datetime.now().strftime('%d')  

    if current_day_full_text == 'Sunday':
        week_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    if current_day_full_text == 'Monday':
        week_days = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    if current_day_full_text == 'Tuesday':
        week_days = ['Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon']
    if current_day_full_text == 'Wednesday':
        week_days = ['Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue']
    if current_day_full_text == 'Thursday':
        week_days = ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed']
    if current_day_full_text == 'Friday':
        week_days = ['Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu']
    if current_day_full_text == 'Sat':
        week_days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri']




    #Getting currently logged-in user maintaining Session

    session = Session.objects.get(session_key=request.session.session_key)
    session_data = session.get_decoded()

    groups = session_data.keys()
    list_group = []
    for grp in groups:
        list_group.append(grp)
        
    if list_group[0] == 'farmer':
        entry = Farmer.objects.get(id=session_data['farmer'])
        firstname = entry.first_name
        lastname = entry.last_name
        email = entry.email
        phone = entry.phone

    if list_group[0] == 'customer':
        entry = Customer.objects.get(id=session_data['customer'])
        firstname = entry.first_name
        lastname = entry.last_name
        email = entry.email
        phone = entry.phone

   


    return render(request, 'weather_data.html',{'latitude':latitude,
                                                'longitude':longitude,
                                                'weather_description':weather_description,
                                                'weather_main':weather_main,
                                                'temp':str("{:.2f}".format(temp)),
                                                'temp_feels_like':str("{:.2f}".format(temp_feels_like)),
                                                'temp_min':str("{:.2f}".format(temp_min)),
                                                'temp_max':str("{:.2f}".format(temp_max)),
                                                'pressure':pressure,
                                                'humidity':humidity,
                                                'visibility':visibility,
                                                'wind_speed':str("{:.2f}".format(wind_speed*1.60934)),
                                                'dire':dire,
                                                'clouds':clouds,
                                                'country':country,
                                                'sunrise':sunrise,
                                                'sunset':sunset,
                                                'city':city,
                                                'day_1':str("{:.2f}".format(day_1)),
                                                'day_2':str("{:.2f}".format(day_2)),
                                                'day_3':str("{:.2f}".format(day_3)),
                                                'day_4':str("{:.2f}".format(day_4)),
                                                'day_5':str("{:.2f}".format(day_5)),
                                                'day_6':str("{:.2f}".format(day_6)),
                                                'weekdays_1':week_days[0],
                                                'weekdays_2':week_days[1],
                                                'weekdays_3':week_days[2],
                                                'weekdays_4':week_days[3],
                                                'weekdays_5':week_days[4],
                                                'weekdays_6':week_days[5],
                                                'month':current_month_text,
                                                'date':current_day,
                                                'year':current_year_full,
                                                'week_day':current_day_full_text,
                                                'firstname':firstname,
                                                'lastname':lastname, 
                                                'email':email, 
                                                'phone':phone})

