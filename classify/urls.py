
from . import views
from django.urls import path,include

urlpatterns = [
    path("pdd",views.index_1,name='index_1'),
    path("predict",views.predictImage,name='predictImage')
]