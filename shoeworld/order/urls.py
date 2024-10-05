from django.urls import path
from .views import *


app_name = 'order'

urlpatterns = [
    path('place_order/',place_order,name='place_order'),
    path('confirmation/',confirmation,name='confirmation'),
    path('concel/<int:pk>/',cancel_order,name='cancel_order'),
    path('return_order/<int:pk>/',return_order,name='return_order'),
    path('individual_return/<int:pk>/', individual_return, name='individual_return'),

    # ---------------------------
    path('list_orders/',admin_orders,name='order_list'),
    path('orders_details/<int:pk>/',admin_order_details,name='admin_order_details'),
    path('order_status/<int:pk>/',order_status,name='order_status'),
    path('completed_payment/',complete_order,name='complete_order'),
    path('admin_cancel_order/<int:pk>/', admin_cancel_order, name='admin_cancel_order'),
    path('admin_return_orders/',admin_return_orders,name='admin_return_orders'),
    path('return_approval/<int:pk>',admin_return_approval,name='return_approval'),


]
