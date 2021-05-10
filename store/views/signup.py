from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from store.models.farmer import Farmer
from store.models.aadhar import Aadharcard
from store.models.weatherdata import Weatherdata
from django.views import View
import requests




class Signup(View):
    
    def get(self, request):
        return render(request, 'signup.html')


    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        group = postData.get('group')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None
        if group == 'customer':
            customer = Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                password=password)
            error_message = self.validateCustomer(customer)

            if not error_message:
                print(first_name, last_name, phone, email, password)
                customer.password = make_password(customer.password)
                customer.register()
                return redirect('homepage')
            else:
                data = {
                    'error': error_message,
                    'values': value
                }
                return render(request, 'signup.html', data)

        else:
            
            aadhar_card_check_no = postData.get('aadhar')
            
            test = Aadharcard.objects.all()
            test_1 = {'test': test}
            aadhcard = []
            for i in test_1['test']:
                aadhcard.append(i.aadhar_card_no)
        
            if aadhar_card_check_no in aadhcard:

                ipinfo = requests.get("https://ipapi.co/json").json()
                lat = ipinfo["latitude"]
                lon = ipinfo["longitude"]

                #coordinates = {"lat": ipinfo["latitude"], "lon": ipinfo["longitude"]}
                #print(coordinates)

                weather = Weatherdata(latitude=lat, phone=phone, longitude=lon)
                weather.save()
          
                farmer = Farmer(first_name=first_name,
                                    last_name=last_name,
                                    phone=phone,
                                    email=email,
                                    password=password)
                error_message = self.validateCustomer(farmer)

                if not error_message:
                    print(first_name, last_name, phone, email, password)
                    farmer.password = make_password(farmer.password)
                    farmer.register()
                    return redirect('homepage')
                else:
                    data = {
                        'error': error_message,
                        'values': value
                    }
                    return render(request, 'signup.html', data)
            else:
                return render(request, 'signup.html')

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message
