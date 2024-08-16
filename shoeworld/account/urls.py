from django.urls import path
from . import views
app_name='account'

urlpatterns = [
    path('',views.user_home,name='user_home'),
    path('user_login/',views.user_login,name='user_login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.register,name='register'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('resend_otp/',views.resend_otp,name='resend_otp'),
    path('single_product/<int:pk>/',views.single_product,name='single_product'),
    path('shop/',views.shop,name='shop'),

]