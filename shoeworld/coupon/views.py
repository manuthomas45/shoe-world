from django.shortcuts import render,redirect,get_object_or_404
from utils.admindecorator import admin_required
from .models import Coupon 
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Coupon

@admin_required
def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'coupon/couponlist.html', {'coupons': coupons})

@admin_required
def create_coupon(request):    
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name').strip()
        minimum_amount = request.POST.get('minimum_amount')
        maximum_amount = request.POST.get('maximum_amount')
        discount = request.POST.get('discount')
        expiry_date = request.POST.get('expiry_date')
        coupon_code = request.POST.get('generated_coupon_code')  
        status = request.POST.get('status')
        if status:
            status = status
        else:
            status=False
    
        errors = []
        try:
            minimum_amount = int(minimum_amount) if minimum_amount else None
            maximum_amount = int(maximum_amount) if maximum_amount else None
            discount = int(discount) if discount else None
        except ValueError:
            errors.append('Minimum Amount, Maximum Amount, and Discount must be valid numbers.')
       
        if not coupon_name:
            errors.append('Coupon Name Required')
        
        if minimum_amount < 10001:
            errors.append('Minimum Amount Should be greater Than ₹10000')
   
        elif minimum_amount > 1000000:
            errors.append('Minimum Amount Should Be Less Than ₹1000000')
 
        if maximum_amount < 3000:
            errors.append('Maximum Amount Should be Greater than ₹3000')

        elif maximum_amount > 10001:
            errors.append('Maximum Amount Only Add Up To ₹10000')

        if minimum_amount is None or maximum_amount is None:
            errors.append('Both Minimum and Maximum Amounts are Required')

        elif minimum_amount < maximum_amount:
            errors.append('Minimum Amount Should be Lesser than Maximum Amount')

        if discount <1:
            errors.append('Discount should be greater than zero')

        elif discount > 65:
            errors.append('Discount Can Only Be Up to 65%')

        if not expiry_date:
            errors.append('Expiry Date is Required')

        if not coupon_code:
            errors.append('Coupon Code is Required')
            
        elif Coupon.objects.filter(coupon_code__iexact=coupon_code).exists():
            errors.append('A Coupon with this Code Already Exists')

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('coupon:coupon_create')

        Coupon.objects.create(
            coupon_name=coupon_name,
            minimum_amount=minimum_amount,
            maximum_amount=maximum_amount,
            discount=discount,
            expiry_date=expiry_date,
            coupon_code=coupon_code,
            status=status   
        )

        messages.success(request, 'Coupon Created Successfully')
        return redirect('coupon:coupon_create')
    else:
        return render(request, 'coupon/createcoupon.html')


@admin_required
def coupon_delete(request, pk): 
    if request.method == 'POST':
        try:
            coupon = get_object_or_404(Coupon, id=pk)
            coupon.status = not coupon.status
            coupon.save()
        except Exception as e:
            messages.error(request, f'Error updating coupon status: {e}')
        return redirect('coupon:coupon_list')

@admin_required
def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, id=pk)
    today = timezone.now().date()  
    
    return render(request, 'coupon/editcoupon.html', {'coupon': coupon, 'today': today})

def edit_coupon_post(request,pk):
    coupon = get_object_or_404(Coupon, id=pk)
    today = timezone.now().date()
    if request.method == 'POST':
        errors = []

        coupon_name = request.POST.get('coupon_name', '').strip()
        minimum_amount = request.POST.get('minimum_amount', '')
        maximum_amount = request.POST.get('maximum_amount', '')
        discount = request.POST.get('discount', '')
        expiry_date = request.POST.get('expiry_date', '')
        coupon_code = request.POST.get('generated_coupon_code', '')
        status = request.POST.get('status') 

        
        try:
            minimum_amount = int(minimum_amount) if minimum_amount else None
            maximum_amount = int(maximum_amount) if maximum_amount else None
            discount = int(discount) if discount else None
        except ValueError:
            errors.append('Minimum Amount, Maximum Amount, and Discount must be valid numbers.')

        if not coupon_code:
            errors.append('Coupon Code is Required')
        elif Coupon.objects.filter(coupon_code__iexact=coupon_code).exclude(id=pk).exists():
            errors.append('A Coupon with this Code Already Exists')

        if minimum_amount:
            if minimum_amount < 20001:
                errors.append('Minimum Amount Should be greater Than ₹20000')
            elif minimum_amount > 1000000:
                errors.append('Minimum Amount Should Be Less Than ₹1000000')
        else:
            errors.append('Minimum Amount is Required')

        if maximum_amount :
            if maximum_amount < 3000:
                errors.append('Maximum Amount Should be Greater than ₹3000')
            elif maximum_amount > 10000:
                errors.append('Maximum Amount Only Add Up To ₹10000')
        else:
            errors.append('Maximum Amount is Required')

        if discount :
            if discount < 1:
                errors.append('Discount should be greater than zero')
            elif discount > 65:
                errors.append('Discount Can Only Be Up to 65%')
        else:
            errors.append('Discount is Required')
            


        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'coupon/editcoupon.html', {'coupon': coupon})

        coupon.coupon_name = coupon_name
        coupon.minimum_amount = minimum_amount
        coupon.maximum_amount = maximum_amount
        coupon.discount = discount
        coupon.expiry_date = expiry_date
        coupon.coupon_code = coupon_code
        if status:
            coupon.status = status
        else:
            coupon.status=False
        coupon.save()

        messages.success(request, 'Coupon Updated Successfully')
        return redirect('coupon:coupon_list')
    
    return render(request, 'coupon/editcoupon.html', {'coupon': coupon, 'today': today})

# ----------------------------------------------user



@require_POST
@login_required
def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code')
    response = {'success': False}

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        current_total = sum(item.total() for item in cart_items)
    except Cart.DoesNotExist:
        response['message'] = 'Cart not found.'
        return JsonResponse(response)

    if coupon_code:
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)

            if current_total >= coupon.minimum_amount:
                discount = coupon.discount
                discount_amount = (current_total * discount / 100)
                discount_amount_total = min(discount_amount, coupon.maximum_amount)
                new_total = current_total - discount_amount_total

                response.update({
                    'success': True,
                    'message': 'Coupon applied successfully.',
                    'current_total': float(current_total),
                    'new_total': float(new_total),
                    'discount': float(discount),
                    'discount_amount': float(discount_amount_total),
                })

                request.session['applied_coupon'] = coupon_code
            else:
                response['message'] = f'Coupon only available for orders over {coupon.minimum_amount}'
        except Coupon.DoesNotExist:
            response['message'] = 'Invalid coupon code.'
    else:
        new_total = sum(item.total() for item in cart_items)
        response.update({
            'success': True,
            'new_total': new_total,
            'discount': 0,
            'discount_amount': 0,
        })

    return JsonResponse(response)



@require_POST  # Ensures the view only handles POST requests
@login_required  # Ensures the user is logged in
def remove_coupon(request):
    response = {'success': False}  # Initialize the response dictionary

    try:
        # Get the user's cart
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        # Remove the applied coupon from the session
        request.session.pop('applied_coupon', None)

        # Calculate the new total after removing the coupon
        new_total = sum(item.total() for item in cart_items)

        # Prepare the response data
        response.update({
            'success': True,
            'message': 'Coupon removed successfully.',
            'new_total': float(new_total),
            'discount': 0
        })
    except Cart.DoesNotExist:
        response['message'] = 'Cart not found.'
    except Exception as e:
        # Catch any other exceptions and return a generic error message
        response['message'] = f'An unexpected error occurred: {str(e)}'

    # Ensure JsonResponse is always returned
    return JsonResponse(response)

