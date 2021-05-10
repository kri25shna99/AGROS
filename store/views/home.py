from django.shortcuts import render , redirect , HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from store.models.farmer import Farmer
from django.views import View
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from store.models.farmorder import Farmorder


# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products()

    #data = {}
    #data['products'] = products
    #data['categories'] = categories
    paginator = Paginator(products,15)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except (EmptyPage, InvalidPage):
        prroducts=paginator.page(paginator.num_pages)


    #Getting currently logged-in user maintaining Session

    session = Session.objects.get(session_key=request.session.session_key)
    session_data = session.get_decoded()
    print(session_data)
    if session_data:
   
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
        
        return render(request, 'index.html', {'products':products,'categories':categories, 'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone})
    else:
        #return render(request, 'index.html', {'products':products,'categories':categories})
        return render(request, 'aboutus.html')
        



def addProducts(request):
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

    categories = Category.get_all_categories()
    #data = {}
    #data['categories'] = categories
    return render(request, 'addProducts.html',{'categories':categories, 'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone})

def form(request):
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


    

    if request.method == 'POST':
        postData = request.POST
        pname = postData.get('pname')
        pprice = postData.get('price')
        pcategory = postData.get('category')
        pdescription = postData.get('description')
        pimage = request.FILES['image']

        farmer = request.session.get('farmer')
 

    
        addprod = Product(name=pname, price=pprice, description=pdescription, image=pimage)
        addcateg = Category(name=pcategory)
        order = Farmorder(farmer=Farmer(id=farmer),product=addprod,category1=pcategory)
    
        addprod.save()
        addcateg.save()
        order.save()

    return render(request, 'addProducts.html',{'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone})


def remedies(request):
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

    return render(request, 'remedies.html',{'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone})


def aboutus(request):

    all_cust = Customer.objects.all()
    all_cust_len = len(all_cust)
    
    all_farm = Farmer.objects.all()
    all_farm_len = len(all_farm)
    
    all_prod = Product.objects.all()
    all_prod_len = len(all_prod)
    
    satisfy_cust_farm = all_cust_len + all_farm_len
    #Getting currently logged-in user maintaining Session

    session = Session.objects.get(session_key=request.session.session_key)
    session_data = session.get_decoded()
    print(session_data)
    if session_data:
        groups = session_data.keys()
        list_group = []
        for grp in groups:
            list_group.append(grp)
        firstname = None
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
    
        return render(request, 'aboutus.html',{'all_cust_len':all_cust_len, 'all_farm_len':all_farm_len, 'all_prod_len':all_prod_len, 'satisfy_cust_farm':satisfy_cust_farm, 'firstname':firstname, 'lastname':lastname, 'email':email, 'phone':phone})
    else:
        return render(request, 'aboutus.html',{'all_cust_len':all_cust_len, 'all_farm_len':all_farm_len, 'all_prod_len':all_prod_len, 'satisfy_cust_farm':satisfy_cust_farm})


