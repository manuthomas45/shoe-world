from django.urls import path
from .views import *


app_name = 'order'

urlpatterns = [
    path('place_order/',order_view,name='place_order'),
    path('confirmation/',confirmation,name='confirmation'),
]
