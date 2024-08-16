from django.urls import path
from . views import *
from . import views

app_name = 'brand'

urlpatterns = [
    path('create/',views.brand_create,name='brand_create'),
    path('list/',views.brand_list,name='brand_list'),
    

]
