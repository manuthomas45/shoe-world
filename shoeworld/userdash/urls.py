from django.urls import path
from .views import *
app_name = 'userdash'

urlpatterns = [
   path('dashboard/',user_dashboard,name="dashboard"),
   path('create_address/',create_address,name='create_address'),
   path('edit_address/<int:pk>/',edit_address,name='edit_address'),
   path('delete/<int:pk>/',delete_address,name='delete_address'),
   path('edit_details/<int:pk>/',edit_details,name='edit_details'),
   path('change_password/',change_password,name='change_password'),
   path('add_wishlist/', add_to_wishlist, name='add_wishlist'),
   path('wishlist/', wishlist, name='wishlist'),
   path('download_invoice/<int:order_id>/', download_invoice, name='download_invoice'),
   path('delete_wishlist_item/<int:pk>/', delete_wishlist_item, name='delete_wishlist_item'),



]