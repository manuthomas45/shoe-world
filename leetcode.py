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
#  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                            #  <div class="tab-pane fade" id="track-orders" role="tabpanel" aria-labelledby="track-orders-tab">
                            #     <div class="card shadow-sm">
                            #         <div class="card-header bg-light d-flex justify-content-between align-items-center py-3">
                            #             <h5 class="mb-0 text-danger font-weight-bold">Wallet</h5>
                            #             <h4 class="mb-0 font-weight-bold">Balance: <span class="text-danger">₹{{ balance }}</span></h4>
                            #         </div>
                            #         <div class="card-body">
                            #             <div class="table-responsive">
                            #                 <table class="table table-hover ">
                            #                     <thead class="thead-light">
                            #                         <tr>
                            #                             <th scope="col">Transaction Type</th>
                            #                             <th scope="col">Amount</th>
                            #                             <th style="width:100px;" scope="col">Date</th>
                            #                             <th scope="col">Description</th>
                            #                         </tr>
                            #                     </thead>
                            #                     <tbody>
                            #                         {% for item in transactions %}
                            #                         <tr>
                            #                             <td>
                            #                                 <span class="badge {% if item.transaction_type == 'Credited' %}badge-success{% else %}badge-danger{% endif %} px-2 py-1">
                            #                                     {{ item.transaction_type }}
                            #                                 </span>
                            #                             </td>
                            #                             <td class="font-weight-bold {% if item.transaction_type == 'Credited' %}text-success{% else %}text-danger{% endif %}">
                            #                                 ₹{{ item.amount }}
                            #                             </td>
                            #                             <td>{{ item.date|date:"M d, Y" }}</td>
                            #                             <td>{{ item.description }}</td>
                            #                         </tr>
                            #                         {% endfor %}
                            #                     </tbody>
                            #                 </table>
                            #             </div>
                            #         </div>
                            #     </div>
                            # </div>  
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
# a=987
# lst=list(str(a))

# print(lst[1])
# d=(int(''.join(lst)))
# print(type(d))
# minPrice = float('inf')  # Start with a very high value (infinity)
# prices = [100, 200, 50, 300]

# for price in prices:

#     minPrice = min(minPrice,price)
# print(minPrice)  # Output will be 50

# nums = [10, 20, 30, 40] 
# nums = [10, 20, 30, 40]
# nums = [10, 20, 30, 40]

# for index, value in enumerate(nums):
#     print(f"Index: {index}, Value: {value}")

# for index, value in enumerate(nums):
#     print(f"Index: {index}, Value: {value}")
# -----------------------------------------------------------------

# @login_required(login_url="/user_login/")
# def payment_success(request):
#     current_user = request.user
#     cart = Cart.objects.get(user=current_user)
#     cart_items = CartItem.objects.filter(cart=cart, is_active=True)
#     cart_total = sum(item.total() for item in cart_items)  # Calculate the total amount
#     user_address = UserAddress.objects.filter(user=current_user)  # Retrieve user addresses

    

# @login_required(login_url="/user_login/")
# def place_order(request):    
#     if request.method == 'POST':
#         current_user = request.user
#         cart = Cart.objects.get(user=current_user)
#         cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
#         selected_address_id = request.POST.get('selected_address')
#         new_total = sum(item.total() for item in cart_items)                                    
        
#         payment_option = request.POST.get('payment_option')
#         user = request.user
#         address = UserAddress.objects.get(id=selected_address_id, user=current_user)
#         current_date_time = datetime.now()
#         formatted_date_time = current_date_time.strftime("%H%m%S%Y")
#         unique = get_random_string(length=4, allowed_chars='1234567890')
#         user = str(request.user.id)
#         order_id = user + formatted_date_time + unique

#         formatted_date_time = current_date_time.strftime("%m%Y%H%S")
#         unique = get_random_string(length=2, allowed_chars='1234567890')
#         payment_id = unique + user + formatted_date_time

#         if not selected_address_id:
#             messages.error(request, 'Select Address To Continue')
#             return redirect('cart:checkout')
        
#         if payment_option == "Cash On Delivery" and new_total > 75000:
#             messages.error(request, 'Cash On Delivery Only Available Upto 75000')
#             return redirect('cart:checkout')
        
#         for cart_item in cart_items:
#             if not cart_item.variant.variant_status:
#                 messages.error(request, 'Select variant')
#                 return redirect('cart:checkout')
            
#             if cart_item.variant.variant_stock < 1:
#                 messages.error(request, 'Out of stock')
#                 return redirect('cart:checkout')
            
#             if not cart_item.product.is_active:
#                 messages.error(request, 'Product inactive')
#                 return redirect('cart:checkout')
        
#         order_address = OrderAddress.objects.create(
#             name=address.name,
#             house_name=address.house_name,
#             street_name=address.street_name,
#             pin_number=address.pin_number,
#             district=address.district,
#             state=address.state,
#             country=address.country,
#             phone_number=address.phone_number
#         )
            
#         order_status = "Confirmed"
            
#         order_main = OrderMain.objects.create(
#             user=current_user,
#             address=order_address,
#             total_amount=new_total,
#             payment_option=payment_option,
#             order_id=order_id,
#             order_status=order_status,
#             payment_id=payment_id,
#             payment_status=True
#         )

#         # Iterate over each cart item to create OrderSub and update variant stock
#         for cart_item in cart_items:
#             OrderSub.objects.create(
#                 user=current_user,
#                 main_order=order_main,
#                 variant=cart_item.variant,
#                 price=cart_item.product.offer_price,
#                 quantity=cart_item.quantity,
#             )
#             # Update the variant stock
#             cart_item.variant.variant_stock -= cart_item.quantity
#             cart_item.variant.save()
        
#         # Delete the cart items after processing
#         cart_items.delete()

#         return redirect('order:confirmation')
#     else:
        # return redirect('cart:checkout')

# 

# 
# 
# 


# {% extends 'userside/base.html' %}
# {% load static %}
# {% block title %}checkout{% endblock title%}
# {% block content %}
# <link href="https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css" rel="stylesheet">

# <section class="checkout_area section_gap" style="margin-top:90px;">
#     <form method="post" action="{% url 'order:place_order' %}">
#         {% csrf_token %}
#     <div class="container">
#         <div class="billing_details">
#             <div class="row">
#                 <!-- Left Column: Billing Details -->
#                 <div class="col-lg-8">
#                         <div class="col-12">
#                             <h3>Select Delivery Address</h3>
#                         </div>
#                         <div class="row address-selection" style="padding-top:20px;">
#                             {% if user_address %}
#                             {% for address in user_address %}
#                             <div class="col-md-6 mb-3">
#                                 <div class="card">
#                                     <div class="card-body">
#                                         <div class="form-check">
#                                             <input class="form-check-input" type="radio" name="selected_address" id="address_{{ address.id }}" value="{{ address.id }}">
#                                             <label class="form-check-label" for="address_{{ address.id }}">
#                                                 <strong>{{ address.name }}</strong><br>
#                                                 {{ address.house_name }},<br> {{ address.street_name }}<br>
#                                                 {{ address.district }}, {{ address.state }} <br>{{ address.pin_number }}<br>
#                                                 {{ address.country }}<br>
#                                                 Phone: {{ address.phone_number }}
#                                             </label>
#                                         </div>
#                                     </div>
#                                 </div>
#                             </div>
#                             {% endfor %}                          
#                         </div>                       
#                 </div>
#                 <div class="col-lg-4">
#                     <div class="order_box">                       
#                         <ul >
#                             <h5 class="mb-3">Payment Method</h5>
#                             <div class="mb-3">
#                                 <div class="form-check mb-2">
#                                     <input class="form-check-input" type="radio" name="payment_option" value="Cash On Delivery" id="Cash On Delivery" checked />
#                                     <label class="form-check-label" for="Cash On Delivery">Cash On Delivery</label>
#                                 </div>
#                                 <div class="form-check mb-2">
#                                     <input class="form-check-input" type="radio" name="payment_option" value="Wallet" id="Wallet" />
#                                     <label class="form-check-label" for="Wallet">Wallet </label>
#                                 </div>
#                                 <div class="form-check">
#                                     <input class="form-check-input" type="radio" name="payment_option" value="Online Payment" id="Online Payment" />
#                                     <label class="form-check-label" for="Online Payment">Online Payment</label>    <img src="{% static 'userside/assets/img/product/card.jpg' %}" alt="" style="margin-left:50px;">

#                                 </div>
#                             </div>
#                             <button type="submit" class="btn btn-warning w-100 mt-3">Place Order</button>
#                             <br>
#                         </ul>
                       
#                     </div>
#                 </div>
#             </div>
#         </div>
#     </div>
# </form>
# </section>
# ------------------------------------
# a=["a","v","b"]
# a.sort()
# c={}
# for i in a:
#         if i>"b":
#            print(ord(i))
# print("".join(a))
print(chr(ord("a")))
print(ord("A"))
print(ord("B"))
print(ord("b"))