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

]