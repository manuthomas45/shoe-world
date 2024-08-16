from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import datetime
from .models import *
from cart.models import *
from userdash.models import *

@login_required(login_url="/user_login/")
def order_view(request):    
    if request.method == 'POST':
        current_user = request.user
        cart = Cart.objects.get(user=current_user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        selected_address_id = request.POST.get('selected_address')
        new_total = sum(item.total() for item in cart_items)                                    
        
        payment_option = request.POST.get('payment_option')
        
       
        
        if not selected_address_id:
            messages.error(request, 'Select Address To Continue')
            return redirect('cart:checkout')
        
        if payment_option == "Cash On Delivery" and new_total > 25000:
            messages.error(request, 'Cash On Delivery Only Available Upto 25000')
            return redirect('cart:checkout')
        
        for cart_item in cart_items:
            if not cart_item.variant.variant_status:
                messages.error(request, 'Select variant')
                return redirect('cart:checkout')
            
            if cart_item.variant.variant_stock < 1:
                messages.error(request, 'Out of stock')
                return redirect('cart:checkout')
            
            if not cart_item.product.is_active:
                messages.error(request, 'Product inactive')
                return redirect('cart:checkout')
        
        return redirect('order:confirmation')
    else:
        return redirect('cart:checkout')
   
def confirmation(request):
    return render(request,'cart/confirmation.html')
   
   

def checkout_view(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        payment_method = request.POST.get('selector')  # Assuming 'selector' is the name for payment method radios
        
        if selected_address_id and payment_method:
            # Process the order with the selected address and payment method
            # ...
            pass
        else:
            messages.error(request, 'Please select an address and payment method.')
    
    # Rest of your view logic
    ...