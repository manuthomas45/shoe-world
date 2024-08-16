from django.urls import path 
from .import views


app_name = 'cart'

urlpatterns = [

  path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
  path('list/', views.cart_list, name='cart'),
  path('checkout/', views.cart_checkout, name='checkout'),
  path('item_delete/<int:pk>/', views.cart_item_delete, name='cart_item_delete'),
  path('update-cart-item/', views.update_cart_item_quantity, name='update_cart_item_quantity'),

  
]
