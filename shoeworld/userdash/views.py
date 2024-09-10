from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .models import UserAddress
from product.models import *
from account.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from order.models import *
from django.http import JsonResponse
import json
from wallet.models import *
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from decimal import Decimal
from io import BytesIO


# Create your views here.

@login_required(login_url='/user_login/')
def create_address(request):
    if request.method == 'POST':
        users = request.user
        name = request.POST.get('name')
        house_name = request.POST.get('house_name')
        street_name = request.POST.get('street_name')
        pin_number = request.POST.get('pin_number')
        district  = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number')
        status = request.POST.get('status') == "on"
        
        address = UserAddress.objects.create(
            user=users,
            name=name,
            house_name=house_name,
            street_name=street_name,
            pin_number=pin_number,
            district=district,
            state=state,
            country=country,
            phone_number=phone_number,
            status=status,
        )
        
        address.save()
        return redirect('userdash:create_address')
    return redirect('userdash:dashboard')


@login_required(login_url='/user_login/')
def user_dashboard(request):
    user = request.user
    user_data = User.objects.get(email=user.email)
    user_address = UserAddress.objects.filter(user=user)
    orders = OrderMain.objects.filter(user=request.user.id).order_by('-id')
    order_sub = OrderSub.objects.filter(user=request.user.id)
    balance = 0  
    wallets = None 
    try:
        wallets = Wallet.objects.get(user=user)
        balance = wallets.balance
    except Wallet.DoesNotExist:
        pass
    
    transactions = Transaction.objects.filter(wallet=wallets)
    return render(request, 'userside/user_dash.html', {
        'user_address': user_address,
        'user_data': user_data,
        'user': user,
        'orders':orders,
        'order_sub':order_sub,
        'balance': balance,
        'transactions':transactions,
        'wallets':wallets,
    })



@login_required(login_url='/user_login/')
def edit_address(request, pk):
    users = get_object_or_404(UserAddress, id=pk)

    if request.method == 'POST':
        users.user = request.user
        users.name = request.POST.get('name')
        users.house_name = request.POST.get('house_name')
        users.street_name = request.POST.get('street_name')
        users.pin_number = request.POST.get('pin_number')
        users.district = request.POST.get('district')
        users.state = request.POST.get('state')
        users.country = request.POST.get('country')
        users.phone_number = request.POST.get('phone_number')

        if users.status:
            UserAddress.objects.filter(user=users.user).update(status=False)
            users.status = request.POST.get('status') == "on"

        users.save()
        return redirect('userdash:dashboard')

    return render(request, 'userdashboard/edit_address.html', {'users': users})



@login_required(login_url='/user_login/')
def delete_address(request, pk):
    if request.method == 'POST':
        address = get_object_or_404(UserAddress, id=pk)
        address.delete()
        
        
        return redirect('userdash:dashboard')
    return HttpResponseNotAllowed(['POST'])


@login_required(login_url='/user_login/')
def edit_details(request, pk):
    user = get_object_or_404(User, id=pk)
    
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')
        
        user.save()
        
        return redirect('userdash:dashboard')
    
    return render(request, 'userside/user_dash.html', {'user': user})



@login_required(login_url='/user_login/')
def change_password(request):
    if request.method == 'POST':
        user = request.user

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if user.check_password(old_password):
            if new_password == confirm_new_password and new_password != old_password:
                user.set_password(new_password) 
                user.save()
                
                messages.success(request, 'Password Changed Successfully')

                user = authenticate(username=request.user.email, password=new_password)
                if user is not None:
                    login(request, user)
                else:
                    messages.error(request, 'Authentication failed. Please login again.')
                    
                return redirect('userdash:change_password')
            else:
                messages.error(request, 'New Passwords Do Not Match or are the Same as the Old Password')
        else:
            messages.error(request, 'Old Password Incorrect')
    
    return render(request, 'userside/user_dash.html')



# -----------------------------------------------wishlist



@login_required(login_url='/user_login/')
def add_to_wishlist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body) 
            variant_id = data.get('variant_id') 
            print("Variant ID:", variant_id) 

            if not variant_id:
                return JsonResponse({'status': 'error', 'message': 'No variant ID provided.'})

            variant = get_object_or_404(ProductVariant, id=variant_id)

            wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, variant=variant)

            if not created:
                return JsonResponse({
                    'status': 'exists',
                    'message': 'This variant is already in your wishlist!'
                })

            return JsonResponse({
                'status': 'success',
                'message': 'Item added to your wishlist!'
            })

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



@login_required(login_url='/user_login/')
def wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    return render(request, 'userdashboard/wishlist.html', {'wishlists': wishlists})


 
    
    
@login_required(login_url='/user_login/')
def delete_wishlist_item(request,pk):
    if request.method == 'POST':
        wishlist_item = get_object_or_404(Wishlist, id=pk, user=request.user)
        print(wishlist_item)
        wishlist_item.delete()

        return redirect('userdash:wishlist') 
    else:
        return redirect('userdash:wishlist')  
    
    
    
@login_required(login_url='/user_login/')
def download_invoice(request, order_id):
    try:
        order_main = get_object_or_404(OrderMain, id=order_id)
        order_sub = OrderSub.objects.filter(main_order=order_main, is_active=True)
        buffer = BytesIO()

        try:
            doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
            elements = []

            styles = getSampleStyleSheet()
            title_style = styles['Heading1']
            subtitle_style = ParagraphStyle(name="Subtitle", fontSize=14, leading=18, spaceAfter=12)
            normal_style = styles['Normal']

            elements.append(Paragraph("SHOE WORLD", title_style))
            elements.append(Paragraph("INVOICE", subtitle_style))
            elements.append(Spacer(1, 0.5 * inch))

            elements.append(Paragraph(f"<b>Order Number:</b> {order_main.order_id}", normal_style))
            elements.append(Paragraph(f"<b>Order Date:</b> {order_main.date.strftime('%B %d, %Y')}", normal_style))
            elements.append(Paragraph(f"<b>Customer Name:</b> {order_main.address.name}", normal_style))
            elements.append(Paragraph(f"<b>Email:</b> {order_main.user.email}", normal_style))
            elements.append(Paragraph(f"<b>Phone:</b> {order_main.address.phone_number}", normal_style))
            elements.append(Paragraph(f"<b>Address:</b> {order_main.address.house_name}, {order_main.address.street_name}, {order_main.address.district}, {order_main.address.state}, {order_main.address.pin_number}, {order_main.address.country}", normal_style))
            elements.append(Spacer(1, 0.5 * inch))

            data = [['Product', 'Quantity', 'Unit Price', 'Discount', 'Total Price']]
            subtotal = Decimal('0.00')
            total_discount = Decimal('0.00')

            for item in order_sub:
                item_total_cost = Decimal(str(item.total_cost()))
                order_total_amount = Decimal(str(order_main.total_amount))
                order_discount_amount = Decimal(str(order_main.discount_amount))

                item_discount_amount = (order_discount_amount * item_total_cost) / order_total_amount
                item_final_price = item_total_cost - item_discount_amount

                subtotal += item_total_cost
                total_discount += item_discount_amount

                data.append([
                    Paragraph(item.variant.product.product_name, normal_style), 
                    str(item.quantity),
                    f"${Decimal(item.price):.2f}",
                    f"-${item_discount_amount:.2f}",
                    f"${item_final_price:.2f}"
                ])

            table = Table(data, colWidths=[None, 1.25 * inch, 1.25 * inch, 1.25 * inch, 1.5 * inch])
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ])
            table.setStyle(style)
            elements.append(table)

            elements.append(Spacer(1, 0.5 * inch))

            total_data = [
                ['Subtotal:', f"${subtotal:.2f}"],
                ['Discount:', f"-${total_discount:.2f}"],
                ['Shipping:', 'Free'],
                ['Total:', f"${subtotal - total_discount:.2f}"]
            ]

            total_table = Table(total_data, colWidths=[4 * inch, 1.5 * inch], hAlign='RIGHT')
            total_table_style = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black)
            ])
            total_table.setStyle(total_table_style)
            elements.append(total_table)

            elements.append(Spacer(1, 1 * inch))
            elements.append(Paragraph("Thank you for shopping with SHOE WORLD!", normal_style))

            doc.build(elements)
        except Exception as e:
            return HttpResponse(f'Error generating PDF content: {str(e)}', status=500)

        buffer.seek(0)
        
        return FileResponse(buffer, as_attachment=True, filename=f'invoice_{order_id}.pdf')

    except Exception as e:
        return HttpResponse(f'Error generating PDF: {str(e)}', status=500)

