from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import datetime
from .models import *
from cart.models import *
from userdash.models import *
from userdash.models import UserAddress
from order.models import OrderAddress,OrderMain,OrderSub
from utils.admindecorator import admin_required
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib import messages
from datetime import datetime
import razorpay
from  coupon.models import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from wallet.models import *
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_control
from django.utils import timezone


@login_required(login_url="/user_login/")
def place_order(request):
    if request.session.get('order_placed'):
          
        return redirect('order:confirmation')
    if request.method == 'POST':
        current_user = request.user
        cart = Cart.objects.get(user=current_user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        coupons = Coupon.objects.filter(status=True, expiry_date__gte=timezone.now()) 

        selected_address_id = request.POST.get('selected_address')
        payment_option = request.POST.get('payment_option')
        cart_total = sum(item.total() for item in cart_items)
        if not selected_address_id:
            messages.error(request, 'Select Address To Continue')
            return redirect('cart:checkout') 
        address = UserAddress.objects.get(id=selected_address_id, user=current_user)

        
        current_date_time = datetime.now()
        formatted_date_time = current_date_time.strftime("%H%m%S%Y")
        unique = get_random_string(length=4, allowed_chars='1234567890')
        user = str(request.user.id)
        order_id = user + formatted_date_time + unique

        formatted_date_time = current_date_time.strftime("%m%Y%H%S")
        unique = get_random_string(length=2, allowed_chars='1234567890')
        payment_id = unique + user + formatted_date_time

       
        if payment_option == "Cash On Delivery" and cart_total > 25000:
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
        if payment_option == "Cash On Delivery":
            
            coupon_code = request.session.get('applied_coupon', None)
            discount = 0
            final_amount = cart_total
            discount_amount = 0
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(coupon_code=coupon_code)
                    discount = coupon.maximum_amount
                    discount_amount = (cart_total * discount / 100)
                    if discount_amount > discount:
                        discount_amount = discount
                    final_amount -= discount_amount
                except Coupon.DoesNotExist:
                    pass
                
            order_address = OrderAddress.objects.create(
                name=address.name,
                house_name=address.house_name,
                street_name=address.street_name,
                pin_number=address.pin_number,
                district=address.district,
                state=address.state,
                country=address.country,
                phone_number=address.phone_number
            )
                
            order_status = "Confirmed"
                
            order_main = OrderMain.objects.create(
                user=current_user,
                address=order_address,
                total_amount=cart_total,
                final_amount=final_amount,
                discount_amount=discount_amount,
                payment_option=payment_option,
                order_id=order_id,
                order_status=order_status,
                payment_id=payment_id,
                payment_status=False,
            )

            for cart_item in cart_items:
                OrderSub.objects.create(
                    user=current_user,
                    main_order=order_main,
                    variant=cart_item.variant,
                    price=cart_item.product.offer_price,
                    quantity=cart_item.quantity,
                )
                cart_item.variant.variant_stock -= cart_item.quantity
                cart_item.variant.save()
            
            cart_items.delete()
            request.session.pop('applied_coupon', None)
            request.session['order_placed'] = True  
            return redirect('order:confirmation')
        elif payment_option == "Online Payment":
            
            coupon_code = request.session.get('applied_coupon', None)
            # discount = 0
            final_amount = cart_total
            # discount_amount = 0
            # if coupon_code:
            #     try:
            #         coupon = Coupon.objects.get(coupon_code=coupon_code)
            #         discount = coupon.maximum_amount
            #         coupon_name = coupon.coupon_name
            #         discount_amount = (cart_total * discount / 100)
            #         if discount_amount > discount:
            #             discount_amount = discount
            #         final_amount-= discount_amount
            #         # order_amount=final_amount
            #     except Coupon.DoesNotExist:
            #         pass
            
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            order_amount = int(final_amount * 100)  
            razorpay_order = client.order.create(dict(
                amount=order_amount,
                currency='INR',
                payment_capture='1'
            ))
            
            razorpay_order_id = razorpay_order['id']
            # order_address = OrderAddress.objects.create(
            #     name=address.name,
            #     house_name=address.house_name,
            #     street_name=address.street_name,
            #     pin_number=address.pin_number,
            #     district=address.district,
            #     state=address.state,
            #     country=address.country,
            #     phone_number=address.phone_number
            #     )
                
            # order_status = "Confirmed"
                    
            # order_main = OrderMain.objects.create(
            #     user=current_user,
            #     address=order_address,
            #     total_amount=cart_total,
            #     final_amount=final_amount,
            #     discount_amount=discount_amount,
            #     payment_option=payment_option,
            #     order_id=order_id,
            #     order_status=order_status,
            #     payment_id=payment_id,
            #     payment_status=True,
            # )

            # for cart_item in cart_items:
            #     OrderSub.objects.create(
            #         user=current_user,
            #         main_order=order_main,
            #         variant=cart_item.variant,
            #         price=cart_item.product.offer_price,
            #         quantity=cart_item.quantity,
            #     )
            #     cart_item.variant.variant_stock -= cart_item.quantity
            #     cart_item.variant.save()
                
            #     cart_items.delete()
            #     request.session.pop('applied_coupon', None)     
            return render(request, 'cart/razorpay.html', {
                'razorpay_key': settings.RAZORPAY_API_KEY,
                'razorpay_order_id': razorpay_order_id,
                'cart_total': cart_total,
                'selected_address_id': selected_address_id
            })
        elif payment_option == "Wallet Payment":
            current_user = request.user
            try:
                wallet = Wallet.objects.get(user=current_user)
                wallet_amount = wallet.balance
                
                cart_items = CartItem.objects.filter(cart__user=request.user, is_active=True)
                new_total = sum(item.total() for item in cart_items)
                
                if new_total <= wallet_amount:
                    wallet = Wallet.objects.get(user=current_user)
                    address = UserAddress.objects.get(id=selected_address_id, user=current_user)
                    payment_option = "Wallet Payment"
                    
                    current_date_time = datetime.now()
                    formatted_date_time = current_date_time.strftime("%H%m%S%Y")
                    unique = get_random_string(length=4, allowed_chars='1234567890')
                    user = str(request.user.id)
                    order_id = user + formatted_date_time + unique
                    
                    formatted_date_time = current_date_time.strftime("%m%Y%H%S")
                    unique = get_random_string(length=2, allowed_chars='1234567890')
                    payment_id = unique + user + formatted_date_time

                    coupon_code = request.session.get('applied_coupon', None)
                    discount = 0
                    final_amount = new_total
                    discount_amount = 0
                    
                    if coupon_code:
                        try:
                            coupon = Coupon.objects.get(coupon_code=coupon_code)
                            discount = coupon.maximum_amount
                            discount_amount = (new_total * discount / 100)
                            if discount_amount > discount:
                                discount_amount = discount
                            final_amount -= discount_amount
                        except Coupon.DoesNotExist:
                            pass
                                
                    order_address = OrderAddress.objects.create(
                        name=address.name,
                        house_name=address.house_name,
                        street_name=address.street_name,
                        pin_number=address.pin_number,
                        district=address.district,
                        state=address.state,
                        country=address.country,
                        phone_number=address.phone_number
                    )
                    
                    order_status = "Confirmed"
                    
                    order_main = OrderMain.objects.create(
                        user=current_user,
                        address=order_address,
                        total_amount=new_total,
                        final_amount=final_amount,
                        discount_amount=discount_amount,
                        payment_option=payment_option,
                        order_id=order_id,
                        order_status=order_status,
                        payment_id=payment_id,
                        payment_status=True
                    )

                    for cart_item in cart_items:
                        OrderSub.objects.create(
                            user=current_user,
                            main_order=order_main,
                            variant=cart_item.variant,
                            price=cart_item.product.offer_price,
                            quantity=cart_item.quantity,
                        )

                        cart_item.variant.variant_stock -= cart_item.quantity
                        cart_item.variant.save()
                        
                    order_amount = new_total
                    description = "Product Purchased With Wallet"
                    transaction_type = "Debited"
                    
                    transaction = Transaction.objects.create(
                        wallet=wallet,
                        description=description,
                        amount=order_amount,
                        transaction_type=transaction_type,
                    )

                    wallet.balance -= final_amount 
                    wallet.save()
                    
                    cart_items.delete()
                    request.session.pop('applied_coupon', None)
                    
                    messages.success(request, 'Order Success')
                    
                    request.session['order_placed'] = True  
                    return redirect('order:confirmation')
                else:
                        messages.error(request, 'Not Enough Money In Wallet')
                        return redirect('cart:cart_checkout')
            except Wallet.DoesNotExist:
                messages.error(request, 'Wallet Does Not Exist')
                return redirect('cart:checkout')
            except Exception as e:
                messages.error(request, str(e))
                return redirect('cart:checkout')

    return redirect('cart:checkout')


@login_required(login_url="/user_login/")
def complete_order(request):
    current_user = request.user
    cart = Cart.objects.get(user=current_user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    cart_total = sum(item.total() for item in cart_items)
    selected_address_id = request.POST.get('selected_address')
    print(selected_address_id)
    address = UserAddress.objects.get(id=selected_address_id, user=current_user)
    print(address)
    current_date_time = datetime.now()
    formatted_date_time = current_date_time.strftime("%H%m%S%Y")
    unique = get_random_string(length=4, allowed_chars='1234567890')
    user = str(request.user.id)
    order_id = user + formatted_date_time + unique

    formatted_date_time = current_date_time.strftime("%m%Y%H%S")
    unique = get_random_string(length=2, allowed_chars='1234567890')
    payment_id = unique + user + formatted_date_time

    if request.session.get('order_placed'):
        return redirect('order:confirmation')
    if request.method == 'POST':
        coupon_code = request.session.get('applied_coupon', None)
        discount = 0
        final_amount = cart_total
        discount_amount = 0
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code)
                discount = coupon.maximum_amount
                coupon_name = coupon.coupon_name
                discount_amount = (cart_total * discount / 100)
                if discount_amount > discount:
                    discount_amount = discount
                final_amount-= discount_amount
                # order_amount=final_amount
            except Coupon.DoesNotExist:
                pass
        
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        order_amount = int(final_amount * 100)  
        razorpay_order = client.order.create(dict(
            amount=order_amount,
            currency='INR',
            payment_capture='1'
        ))
        
        razorpay_order_id = razorpay_order['id']
        order_address = OrderAddress.objects.create(
            name=address.name,
            house_name=address.house_name,
            street_name=address.street_name,
            pin_number=address.pin_number,
            district=address.district,
            state=address.state,
            country=address.country,
            phone_number=address.phone_number
            )
            
        order_status = "Confirmed"
        payment_option = "Online Payment"
        order_main = OrderMain.objects.create(
            user=current_user,
            address=order_address,
            total_amount=cart_total,
            final_amount=final_amount,
            discount_amount=discount_amount,
            payment_option=payment_option,
            order_id=order_id,
            order_status=order_status,
            payment_id=payment_id,
            payment_status=True,
        )

        for cart_item in cart_items:
            OrderSub.objects.create(
                user=current_user,
                main_order=order_main,
                variant=cart_item.variant,
                price=cart_item.product.offer_price,
                quantity=cart_item.quantity,
            )
            cart_item.variant.variant_stock -= cart_item.quantity
            cart_item.variant.save()
            
            cart_items.delete()
            request.session.pop('applied_coupon', None)   
        current_user = request.user
        cart = Cart.objects.get(user=current_user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        selected_address_id = request.POST.get('selected_address')
        cart_total = float(request.POST.get('cart_total'))
        
        
        if payment_option == "Online Payment":
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            try:
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature,

                }
                client.utility.verify_payment_signature(params_dict)
                
            except razorpay.errors.SignatureVerificationError:
                messages.error(request, "Payment verification failed. Please try again.")
                return redirect('cart:checkout')  
        request.session['order_placed'] = True           
        return redirect('order:confirmation')

    return redirect('cart:checkout')




@login_required(login_url="/user_login/")
def cancel_order(request, pk):
    try:
        order = get_object_or_404(OrderMain, id=pk)
        order_items = OrderSub.objects.filter(main_order=order, is_active=True)
        
        if not order.is_active:
            messages.error(request, 'Order item is already Canceled.')
            return redirect('userdash:dashboard')
        
        for order_item in order_items:
            order_variant = order_item.variant
            order_quantity = order_item.quantity
            
            order_variant.variant_stock += order_quantity
            order_variant.save()
        
        order.order_status = "Canceled"
        order.is_active = False
        order.save()
        if order.payment_option in ["Online Payment", "Wallet Payment"]:
            item_refund = Decimal('0')

            for item in order_items:
                item_amount = Decimal(str(item.price * item.quantity))
                order_amount = Decimal(str(order.total_amount))
                order_discount_amount = Decimal(str(order.discount_amount))

                item_discount_amount = (order_discount_amount * item_amount) / order_amount
                item_refund_amount = item_amount - item_discount_amount

                item_refund += item_refund_amount
                item.is_active = False
                item.main_order.final_amount -= item_refund
                item.save()

            if item_refund > 0:
                description = f"Refund for Cancel order {order.order_id}"
                transaction_type = "Credited"

                wallet, created = Wallet.objects.get_or_create(user=request.user)

                transaction = Transaction.objects.create(
                    wallet=wallet,
                    description=description,
                    amount=item_refund,
                    transaction_type=transaction_type,
                )

                wallet.balance += item_refund  # Ensure Decimal type for accurate calculation
                wallet.save()

            order.final_amount -= item_refund
            order.save()

        
        messages.success(request, 'Order has been successfully canceled.')
        
    except OrderMain.DoesNotExist:
        messages.error(request, 'Order does not exist.')
    
    return redirect('userdash:dashboard')



@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@login_required(login_url="/user_login/")
def confirmation(request):
    
    
    return render(request,'cart/confirmation.html')
 


@login_required(login_url="/user_login/")
def return_order(request, pk):
    try:
        # Fetch the order
        order = get_object_or_404(OrderMain, id=pk)
        order_items = OrderSub.objects.filter(main_order=order)
        
        # Check if the order is already returned
        if not order.is_active:
            messages.error(request, 'Order item is already returned.')
            return redirect('userdash:dashboard')
        
        # Check if the order is in a non-returnable status
        if order.order_status in ['Pending', 'Confirmed', 'Shipped']:
            messages.error(request, 'Order cannot be returned at this stage.')
            return redirect('userdash:dashboard')
        
        # Get the reason for the return from the request
        reason = request.POST.get('reason', '').strip()
        if not reason:
            messages.error(request, 'A reason must be provided for returns.')
            return redirect('userdash:dashboard')
        
        # Create a return request
        ReturnRequest.objects.create(
            order_main=order,
            reason=reason
        )
        
        # Update the order status
        order.order_status = "Pending"
        order.save()
        
        messages.success(request, "Please wait for the admin's approval.")
        return redirect('userdash:dashboard')
    
    except OrderMain.DoesNotExist:
        messages.error(request, "Order does not exist.")
    
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
    
    return redirect('userdash:dashboard')

#  ------------------------------------------------------------------------admin order area|

@admin_required
def admin_orders(request):
    search_query = request.GET.get('search', '').strip()
    if search_query:
        orders = OrderMain.objects.filter(order_id__icontains=search_query)
    else:
        orders = OrderMain.objects.all().order_by('-id')
    return render(request, 'order/admin_order.html', {'orders': orders, 'search_query': search_query})





@admin_required
def admin_order_details(request, pk):
    orders = get_object_or_404(OrderMain, id=pk)
    order_sub = OrderSub.objects.filter(main_order=orders)
    return render(request, 'order/admin_order_details.html', {'orders': orders, 'order_sub': order_sub})




@admin_required
def order_status(request, pk):
    order = get_object_or_404(OrderMain, id=pk)
    
    order_items = OrderSub.objects.filter(main_order=order, is_active=True)
    new_status = request.POST.get('order_status')
    
    if new_status:
        order.order_status = new_status
        order.save()
        
        # if new_status=="Canceled":
        #     for order_item in order_items:
        #         order_variant = order_item.variant
        #         order_quantity = order_item.quantity
                
        #         order_variant.variant_stock += order_quantity
        #         order_variant.save()
        return redirect('order:admin_order_details', pk)
        
    else:
        return redirect('order:admin_order')
    

@admin_required
def admin_cancel_order(request, pk):
    try:
        # Fetch the main order object
        order = get_object_or_404(OrderMain, id=pk)
        # Fetch all active order items related to the main order
        order_items = OrderSub.objects.filter(main_order=order, is_active=True)

        # Loop through order items and update variant stock
        for order_item in order_items:
            order_variant = order_item.variant
            order_quantity = order_item.quantity
            order_variant.variant_stock += order_quantity
            order_variant.save()  # Save the updated stock back to the database

        # Set order status to "Canceled"
        order.order_status = "Canceled"
        order.save()

        refund_amount = Decimal('0.00')

        # Check if the payment option requires a refund
        if order.payment_option in ["Online Payment", "Wallet Payment"]:
            for item in order_items:
                item_total_cost = Decimal(str(item.final_total_cost()))
                order_total_amount = Decimal(str(item.main_order.total_amount))
                order_discount_amount = Decimal(str(item.main_order.discount_amount))

                item_discount_amount = (order_discount_amount * item_total_cost) / order_total_amount
                item_refund_amount = item_total_cost - item_discount_amount

                refund_amount += item_refund_amount
                item.is_active = False  # Mark order item as inactive
                item.save()

            if refund_amount > 0:
                description = f"Sorry Due To Some Reason Admin Canceled This Order {order.order_id}"
                transaction_type = "Credited"

                # Get or create wallet for the user
                wallet, created = Wallet.objects.get_or_create(user=order.user)

                # Create a transaction
                transaction, created = Transaction.objects.get_or_create(
                    wallet=wallet,
                    description=description,
                    amount=refund_amount,
                    transaction_type=transaction_type,
                )

                # Update the wallet balance
                wallet.balance += refund_amount
                wallet.save()

            # Deduct refund amount from the order's final amount
            order.final_amount -= refund_amount
            order.save()

            # Display success message
            messages.success(request, 'Order Canceled and credited to the user\'s wallet.')
            return redirect('order:admin_order_details', pk=order.id)

        else:
            # Display success message for non-refundable payment options
            messages.success(request, 'Order Canceled Successfully')
            return redirect('order:admin_order_details', pk=order.id)

    except OrderMain.DoesNotExist:
        # Handle the case where the order does not exist
        messages.error(request, 'Order does not exist.')
        return redirect('admin_panel:admin_order_details', pk=order.id)

    # Redirect to order details page if something goes wrong
    return redirect('admin_panel:admin_order_details', pk=order.id)




@admin_required
def admin_return_orders(request):
    return_requests = ReturnRequest.objects.all().order_by('-created_at')

    return render(request, 'order/return.html', {'return_requests': return_requests,})




def return_approval(request, pk):
    if request.method == "POST":
        return_request = get_object_or_404(ReturnRequest, id=pk)
        action = request.POST.get('action')

        if action == 'Approve':
            return_request.status = "Approved"
            return_request.save()

            refund_amount = Decimal('0.00')

            order = return_request.order_main
            active_items = order.ordersub_set.filter(is_active=True)

            for item in active_items:
                item_total_cost = Decimal(str(item.final_total_cost()))
                order_total_amount = Decimal(str(order.total_amount))
                order_discount_amount = Decimal(str(order.discount_amount))

                item_discount_amount = (order_discount_amount * item_total_cost) / order_total_amount
                item_refund_amount = item_total_cost - item_discount_amount

                refund_amount += item_refund_amount
                item.is_active = False
                item.status = "Returned"
                item.save()

            order.order_status = 'Returned'
            order.is_active = False
            order.final_amount -= refund_amount
            order.save()

            # Handle refund to wallet if applicable
            if refund_amount > 0 and return_request.order_main.payment_status:
                wallet, created = Wallet.objects.get_or_create(user=return_request.order_main.user)
                wallet.balance += refund_amount
                wallet.updated_at = timezone.now()
                wallet.save()

                Transaction.objects.create(
                    wallet=wallet,
                    amount=float(refund_amount),
                    description=f"Refund for {'order' if return_request.order_sub is None else 'item'} {return_request.order_main.order_id if return_request.order_sub is None else return_request.order_sub.variant.product.product_name}",
                    transaction_type='Credited'
                )

                messages.success(request, 'Return request approved and amount credited to the user\'s wallet.')
                return redirect('order:admin_return_orders')
            else:
                messages.success(request, 'Return request approved. No payment was made or payment status is not confirmed.')
                return redirect('order:admin_return_orders')

        elif action == "Reject":
            return_request.status = "Rejected"          
            return_request.save()
            messages.success(request, 'Return request rejected.')
            return redirect('order:admin_return_orders')

        else:
            messages.error(request, 'Invalid action.')
            return redirect('order:admin_return_orders')

    return redirect('order:admin_return_orders')
