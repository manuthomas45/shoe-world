from django.urls import path
from .views import *
app_name = 'product'

urlpatterns = [
    path('create/',product_create, name='product_create'),
    path('list/', product_view, name='product_view'),
    path('info/<int:pk>/',product_info, name='product_info'),
    path('delete/<int:pk>/', product_delete, name='product_delete'),
    path('edit/<int:pk>/', product_edit, name='product_edit'),
    path('image/<int:pk>/', product_image, name='product_image'),
    path('image_delete/<int:pk>/',delete_image , name='image_delete'),
    path('variants/<int:pk>/', variants_view, name='product_variant'),
    path('create_variants/<int:pk>/', variant_create, name='create_variant'),
    path('edit_variant/<int:pk>/', variant_edit, name='variant_edit'),
    path('variant_status/<int:pk>/', variant_status, name='variant_status'),
    path('review/<int:pk>/',review_create,name='product_review'),
    path('review_delete/<int:pk>/', delete_review, name='review_delete'),

   
]
