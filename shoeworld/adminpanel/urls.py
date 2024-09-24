from django.urls import path

from adminpanel import views

urlpatterns = [
  path('adminpanel/',views.admin_dashboard,name="adminpanel"),
  path('admin_login/',views.admin_login, name='admin_login'),
  path('admin_logout/',views.admin_logout, name='admin_logout'),
  path('user_list/',views.user_list, name='user_list'),
  path('user-block/<int:user_id>/',views.user_block, name='user_block'),
  path('user-unblock/<int:user_id>/',views.user_unblock, name='user_unblock'),
  path('sales_report/',views.sales_report, name='sales_report'),
  path('sales_report/date_filter/',views.order_date_filter, name='date_filter'),
  path('best_selling_products/',views.best_selling_products, name='best_selling_product'),
  path('best_selling_categories/',views.best_selling_categories, name='best_selling_categories'),
  path('best_selling_brands/',views.best_selling_brands, name='best_selling_brands'),

  
]

    
