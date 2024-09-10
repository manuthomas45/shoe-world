from django.urls import path
from .views import *

app_name = 'coupon'

urlpatterns = [
    path('list/',coupon_list,name='coupon_list'),
    path('create/',create_coupon,name='coupon_create'),
    path('delete/<int:pk>/', coupon_delete, name='coupon_delete'),
    path('edit/<int:pk>/', edit_coupon, name='edit_coupon'),
    # ------------------
    path('apply_coupon',apply_coupon,name='apply_coupon'),
    path('remove_coupon',remove_coupon,name='remove_coupon'),
]
