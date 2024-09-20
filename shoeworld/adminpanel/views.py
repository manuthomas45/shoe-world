from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout 
from django.contrib import messages
from account.models import User
from utils.admindecorator import admin_required
from django.utils import timezone
from order.models import  *
from django.db.models import Sum,Count
from datetime import datetime
from datetime import timedelta




# Create your views here.


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_admin:
                login(request, user)
                return redirect('adminpanel') 
            else:
                messages.error(request, 'You are not authorized to access this page.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'adminside/admin_login.html')

@admin_required
def user_list(request):
    users = User.objects.filter(is_admin=False).order_by('id')
    return render(request, 'adminside/user_list.html', {'users': users})

@admin_required
def user_block(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = True
    user.save()
    return redirect('user_list')

@admin_required
def user_unblock(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_blocked = False
    user.save()
    return redirect('user_list')

@admin_required
def adminpanel(request):
    return render(request,'adminside/index.html')

@admin_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login') 


@admin_required
def sales_report(request):
    filter_type = request.GET.get('filter', None)
    now = timezone.now()
    start_date = end_date = None  # Initialize to None

    if filter_type == 'weekly':
        start_date = now - timedelta(days=now.weekday())
        end_date = now
    elif filter_type == 'monthly':
        start_date = now.replace(day=1)
        end_date = now

    # Filter orders based on whether a date range is defined
    if start_date and end_date:
        orders = OrderMain.objects.filter(
            order_status="Delivered",
            is_active=True,
            date__range=[start_date, end_date]
        )
    else:
        # No specific filter, show all "Order Placed" orders
        orders = OrderMain.objects.filter(
            order_status="Delivered",
            is_active=True
        )

    total_discount = orders.aggregate(total=Sum('discount_amount'))['total']
    total_orders = orders.aggregate(total=Count('id'))['total']
    total_order_amount = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    return render(request, 'adminside/salesreport.html', {
        'orders': orders,
        'total_discount': total_discount,
        'total_orders': total_orders,
        'total_order_amount': total_order_amount
    })


@admin_required
def order_date_filter(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return redirect('admin_panel:sales_report')

            orders = OrderMain.objects.filter(
                date__range=[start_date, end_date], 
                order_status="Delivered"
            )
            total_discount = orders.aggregate(total=Sum('discount_amount'))['total']
            total_orders = orders.aggregate(total=Count('id'))['total']
            total_order_amount = orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

            return render(request, 'adminside/salesreport.html', {
                'orders': orders,
                'total_discount': total_discount,
                'total_orders': total_orders,
                'total_order_amount': total_order_amount
            })

    return redirect('sales_report')