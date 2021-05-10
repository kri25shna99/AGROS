from django.contrib import admin
from django.urls import path
from .views.home import Index , store, addProducts, form, remedies, aboutus
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut
from .views.orders import OrderView
from .views.farmorder import FarmOrderView, deleteprod
from .views.weather import weathsms, weatherdatas
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    #path('weatherdatas', weathsms, name='weathsms'),
    path('store', store , name='store'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('farmorder', FarmOrderView.as_view(), name='farmorder'),
    path('addProducts', addProducts , name='addProducts'),
    path('form', form , name='form'),
    path('remedies', remedies , name='remedies'),
    path('aboutus', aboutus , name='aboutus'),
    path('weatherdatas', weatherdatas , name='weatherdatas'),
    path('delete/<int:id>', deleteprod , name='deleteprod'),
]
