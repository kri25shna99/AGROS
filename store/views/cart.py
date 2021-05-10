from django.shortcuts import render , redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View
from store.models.product import  Product

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        #print(products)
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

        return render(request , 'cart.html' , {'products' : products,'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone} )

