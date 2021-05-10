from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Product
from store.models.orders import Order
from store.middlewares.auth import auth_middleware

class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        #print(customer)
        #Getting currently logged-in user maintaining Session

        session = Session.objects.get(session_key=request.session.session_key)
        session_data = session.get_decoded()

        groups = session_data.keys()
        list_group = []
        for grp in groups:
            list_group.append(grp)
            

        entry = Customer.objects.get(id=session_data['customer'])
        firstname = entry.first_name
        lastname = entry.last_name
        email = entry.email
        phone = entry.phone
    


        return render(request , 'orders.html'  , {'orders' : orders,'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone})
