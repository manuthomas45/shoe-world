from django.urls import path 
from . import views


app_name = 'category'

urlpatterns = [

  path('list_category/',views.list_category,name='list_category'),
  path('create/',views.create_category,name='create_category'),
  path('edit/<int:pk>/',views.edit_category,name='edit_category'),
  path('delete/<int:pk>/',views.delete_category,name='delete_category'),

]
