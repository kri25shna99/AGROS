from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import check_password
from store.models.farmer import Farmer
from django.views import View
from store.models.product import Product
from store.models.farmorder import Farmorder
from store.middlewares.auth import auth_middleware


class FarmOrderView(View):

    def get(self , request ):
        farmer = request.session.get('farmer')
        orders = Farmorder.get_orders_by_farmer(farmer)
        #print(farmer)
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

   

        return render(request , 'farmorder.html'  , {'orders' : orders,'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone})




def deleteprod(request, id=None):
    prod = Product.objects.get(id=id)
    prod.delete()
    return redirect('farmorder')

