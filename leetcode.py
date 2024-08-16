# arr = [3, 1, 2]
# b=[5,9,1,6]
# a = arr.sort()
# print(a)
# print(arr)
# print(sorted(b))
# print(b)
# a="ksjlk lksjflj lskfjlksj l;skjh"
# b=a.split()
# c=len(b)
# print(b[-1])
# print(b[-2])
# numbers = [5, 6, 4, 7, 3, 8, 2, 1]
# def print_pattern(numbers):
#     size = 4
#     grid = [[' ' for _ in range(size * 2 - 1)] for _ in range(size)]
#     grid[0][size-1] = str(numbers[0])
#     grid[1][size-2] = str(numbers[1])
#     grid[1][size] = str(numbers[2])
#     grid[2][size-3] = str(numbers[3])
#     grid[2][size+1] = str(numbers[4])
#     grid[3][size-4] = str(numbers[5])
#     grid[3][size-2] = str(numbers[6])
#     grid[3][size] = str(numbers[7])
#     for row in grid:
#         print(''.join(row))
# print_pattern(numbers)

# s = ["h","e","l","l","o"]

# p=s[::-1]
            
# print(p)      
# s="lahdfjkg"
# for i in s:
#     print (i,end="")      
# s="ksjd"
# m1=[]
# for i in s:
#             m1.append(s.index(i))
# print(m1)
# s = "foo"
# t = "bar"
# class Solution:
#     def isIsomorphic(self, s: str, t: str) -> bool:
#         m1=[]
#         m2=[]
#         for i in s:
#             m1.append(s.index(i))
            
#         for i in t:
#             m2.append(t.index(i))
            
#         if m1==m2 :
#             return True
       
#         return (False,m1,m2)
# a=Solution()
# b=a.isIsomorphic(s,t)
# print(b,m1,m2)
# int
a=987
lst=list(str(a))

print(lst[1])
d=(int(''.join(lst)))
print(type(d))
# minPrice = float('inf')  # Start with a very high value (infinity)
# prices = [100, 200, 50, 300]

# for price in prices:
#     minPrice = min(minPrice,price)

# print(minPrice)  # Output will be 50

class OrderVerificationView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect('cart:cart_checkout')
    
    def post(self, request):
        current_user = request.user
        cart = Cart.objects.get(user=current_user)
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        address = UserAddress.objects.get(user=current_user, order_status=True,is_deleted=False)  
        new_total = sum(item.sub_total() for item in cart_items)                                    
        
        payment_option = request.POST.get('payment_option')
        
        if payment_option is None:
            messages.error(request, 'Select Payment Option')
            return redirect('cart:cart_checkout')
        
        if not address:
            messages.error(request, 'Select Address To Continue')
        
        if payment_option == "Cash On Delivery" and new_total > 6000:
            messages.error(request, 'Cash On Delivery Only Available Upto 6000')
            return redirect('cart:cart_checkout')
        
        for cart_item in cart_items:
            if not cart_item.variant.variant_status:
                messages.error(request, 'Select variant')
                return redirect('cart:cart_checkout')
            
            if cart_item.variant.variant_stock < 1:
                messages.error(request, 'Out of stock')
                return redirect('cart:cart_checkout')
            
            if not address.status:
                messages.error(request, 'Select address')
                return redirect('cart:cart_checkout')
            
            if not cart_item.product.is_active:
                messages.error(request, 'Product inactive')
                return redirect('cart:cart_checkout')
        
        coupon_code = request.session.get('applied_coupon', None)
        discount = 0
        
        if payment_option == "Online Payment":
            return redirect('order:online_payment')
        
        if payment_option == "Wallet" and new_total > 6000:
                current_user = request.user
                try:
                    wallet = Wallet.objects.get(user=current_user)
                    wallet_amount = wallet.balance
                    
                    cart_items = CartItem.objects.filter(cart__user=request.user, is_active=True)
                    new_total = sum(item.sub_total() for item in cart_items)
                    
                    if new_total <= wallet_amount:
                        wallet = Wallet.objects.get(user=current_user)
                        address = UserAddress.objects.get(user=current_user, order_status=True)
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
                                if new_total >= coupon.minimum_amount:
                                    discount = coupon.discount
                                    discount_amount = (new_total * discount / 100)
                                    # Cap the discount amount to the maximum amount
                                    discount_amount = min(discount_amount, coupon.maximum_amount)
                                    
                                    final_amount = new_total - discount_amount
                                    request.session['applied_coupon'] = coupon_code
                                else:
                                    messages.error(request, f'Coupon only available for orders over {coupon.minimum_amount}')
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

                        wallet.balance -= order_amount 
                        wallet.save()
                        
                        cart_items.delete()
                        
                        request.session['order_id'] = order_main.order_id
                        request.session['order_date'] = order_main.date.strftime("%Y-%m-%d")
                        request.session['order_status'] = order_main.order_status
                        
                        request.session.pop('applied_coupon', None)
                        
                        messages.success(request, 'Order Success')
                        
                        return redirect('order:order_success')
                    else:
                        messages.error(request, 'Not Enough Money In Wallet')
                        return redirect('cart:cart_checkout')
                except Wallet.DoesNotExist:
                    messages.error(request, 'Wallet Does Not Exist')
                    return redirect('cart:cart_checkout')
                except Exception as e:
                    messages.error(request, str(e))
                    return redirect('cart:cart_checkout')
        else:
            
            user = request.user
            cart_items = CartItem.objects.filter(cart__user=user, is_active=True) 
            new_total = sum(item.sub_total() for item in cart_items) 
            
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

            cart_items.delete()
            
            request.session['order_id']=order_main.order_id
            request.session['order_date'] = order_main.date.strftime("%Y-%m-%d")
            request.session['order_status']=order_main.order_status
            
            request.session.pop('applied_coupon', None)
            
            messages.success(request, 'Order Success')
            
            return redirect('order:order_success')

