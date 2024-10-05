from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from product.models import *
from .models import *
import json
from cart.models import *
from userdash.models import *
from django.contrib import messages
from coupon.models import Coupon,UserCoupon
from django.views.decorators.cache import cache_control


@require_POST
@csrf_protect
@login_required(login_url='/user_login/')
def add_to_cart(request):
    
    try:
        data = json.loads(request.body)
        variant_id = data.get('variant_id')
        quantity = int(data.get('quantity', 1))

        if not all([variant_id, quantity]):
            return JsonResponse({'success': False, 'message': 'Missing required fields'}, status=400)

        variant = ProductVariant.objects.get(id=variant_id)
        product =Products.objects.get(id=variant.product.id)

        
        
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )

        if not item_created:
            if cart_item.quantity>=5:
                return JsonResponse({'success': False, 'message': 'You cannot add more than 5 items'}, status=404)
            else:              
                cart_item.quantity += quantity
                cart_item.save()

        return JsonResponse({'success': True, 'message': 'Item added to cart successfully'})

    except ProductVariant.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product variant not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='/user_login/')
def cart_list(request):
    if request.session.get('order_placed'): 
        del request.session['order_placed']

    try:
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = CartItem.objects.filter(cart=cart)
        cart_prices = CartItem.objects.filter(cart=cart, is_active=True)
        cart_total = sum(item.total() for item in cart_prices)
        

        return render(request, 'cart/cart.html', {
            'cart': cart, 
            'cart_item': cart_item, 
            'cart_total': cart_total, 
        })
    except Exception as e:
        # print(f"Error: {e}")  
        return render(request, 'cart/cart.html')


def update_cart_item_quantity(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('quantity'))

        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = new_quantity
        cart_item.save()

        cart = cart_item.cart
        subtotal = sum(item.total() for item in cart.cart.all())
        total = cart_item.total()
        return JsonResponse({
            'subtotal': f'{subtotal:.2f}',
            'total': f'{total:.2f}',
            'quantity': cart_item.quantity,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

    
@login_required(login_url='/user_login/')
def cart_item_delete(request,pk):
    cart_item=CartItem.objects.filter(id=pk)
    cart_item.delete()
    return redirect('cart:cart')

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url='/user_login/')
def cart_checkout(request):
    if request.session.get('order_placed'):
          
        return redirect('order:confirmation')     
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)         
    available_coupons = Coupon.objects.filter(status=True, expiry_date__gte=timezone.now()) 
    used_coupons = UserCoupon.objects.filter(user=request.user).values_list('coupon', flat=True) 
    coupons = available_coupons.exclude(id__in=used_coupons)


    for cart_item in cart_items:
        if not cart_item.variant.variant_status:
            messages.error(request, 'Variant unavailable')
            return redirect('cart:cart')
        
        if cart_item.variant.variant_stock < 1:
            messages.error(request, 'Out of stock')
            return redirect('cart:cart')
        
        if not cart_item.product.is_active:
            messages.error(request, 'Product unavailable')
            return redirect('cart:cart')
    
    if not cart_items.exists():
            # messages.error(request, "No valid items found in cart. Please try again.")
            return redirect('account:shop')
    cart_total = sum(item.total() for item in cart_items)
    
   
    user_address = UserAddress.objects.filter(user=request.user.id)
    

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'user_address': user_address,
        'coupons':coupons,
    })
