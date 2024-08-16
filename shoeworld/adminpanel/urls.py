from django.urls import path

from adminpanel import views

urlpatterns = [
  path('dashboard/',views.adminpanel,name="adminpanel"),
  path('admin_login/',views.admin_login, name='admin_login'),
  path('admin_logout/',views.admin_logout, name='admin_logout'),
  path('user_list/',views.user_list, name='user_list'),
  path('user-block/<int:user_id>/',views.user_block, name='user_block'),
  path('user-unblock/<int:user_id>/',views.user_unblock, name='user_unblock'),



]

    
