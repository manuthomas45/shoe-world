from django.shortcuts import render,redirect,get_object_or_404
from .form import * 
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from dateutil.parser import parse  # Importing dateutil
from datetime import timedelta
from django.contrib.auth import login, logout
from product.models import *
from django.db.models import Avg
from categoryy.models import Category
from brand.models import Brand



def user_login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active and not user.is_blocked:  
                login(request, user)
                # messages.success(request, f"Welcome, {user.email}! You have successfully logged in.")
                return redirect('account:user_home')
            else:
                messages.error(request, "This account is blocked. Please contact support.")
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    else:
        form = EmailAuthenticationForm()
    return render(request, 'userside/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            
            user_data = form.save(commit=False)
            otp = get_random_string(length=6, allowed_chars='1234567890')
            print(otp)
            otp_generation_time = timezone.now().isoformat()
            request.session['otp'] = otp
            request.session['otp_generation_time'] = otp_generation_time         
            user_data.is_active = False

            request.session['user_data'] = {
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'email': user_data.email,
                'phone_number': user_data.phone_number,
                'password': form.cleaned_data.get('password')  
            }
            
            try:
                send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user_data.email],
                fail_silently=False,
            )
                
                messages.success(request, 'OTP has been sent to your email. Please verify to complete registration.')
                return redirect('account:verify_otp')
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, 'Enter a valid email ID')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = UserRegistrationForm()
    return render(request, 'userside/register.html', {'form': form})



def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_generation_time_str = request.session.get('otp_generation_time')

        if otp_generation_time_str:
            try:
                otp_generation_time = parse(otp_generation_time_str)
                current_time = timezone.now()
                otp_valid_duration = timedelta(minutes=2)

                if current_time - otp_generation_time <= otp_valid_duration:
                    if otp == request.session.get('otp'):
                        user_data = request.session.get('user_data')
                        if user_data:
                            user = User.objects.create(
                                first_name=user_data.get('first_name'),
                                last_name=user_data.get('last_name'),
                                email=user_data.get('email'),
                                phone_number=user_data.get('phone_number')
                            )
                            user.set_password(user_data.get('password'))  
                            user.is_active = True
                            user.save()

                            request.session.flush()

                            messages.success(request, 'Your account has been activated successfully.')
                            return redirect('account:user_login') 
                        else:
                            messages.error(request, 'User data not found. Please register again.')
                    else:
                        messages.error(request, 'Invalid OTP. Please try again.')
                else:
                    messages.error(request, 'OTP has expired. Please resent OTP.')
            except ValueError:
                messages.error(request, 'Invalid OTP generation time format.')
        else:
            messages.error(request, 'OTP generation time not found. Please register again.')
    

    return render(request, 'userside/verify_otp.html')


def resend_otp(request):
    user_data = request.session.get('user_data')
    if user_data:
        otp = get_random_string(length=6, allowed_chars='1234567890')
        otp_generation_time = timezone.now().isoformat()
        print(otp)
        
        request.session['otp'] = otp
        request.session['otp_generation_time'] = otp_generation_time

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [user_data['email']],
            fail_silently=False,
        )
        messages.success(request, 'A new OTP has been sent to your email.')
    else:
        messages.error(request, 'User data not found. Please register again.')
    return redirect('account:verify_otp')

# --------------------------------



def user_home(request):
    products=Products.objects.all()
    return render(request,'userside/index.html',{'products':products})


def single_product(request,pk):
    product=get_object_or_404(Products,pk=pk)
    image=ProductImages.objects.filter(product=product)
    category=Category.objects.get(category_name=product.product_category)
    brand=Brand.objects.get(brand_name=product.product_brand)
    variants =ProductVariant.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)

    return render(request,'userside/single_product.html',{'products':product,'images':image,'category':category,'brand':brand,'variants':variants,'reviews':reviews})



def shop(request):
    search_query = request.GET.get('search', '')
    
    selected_category = request.GET.get('category')
    selected_brand = request.GET.get('brand')
    
    sort_option = request.GET.get('sort', '')
    
    products = Products.objects.all()
    if search_query:
        products = products.filter(product_name__icontains=search_query)
    
    if selected_category and selected_category != 'all' and selected_category.isdigit():
        products = products.filter(product_category__id=selected_category)
    
    if selected_brand and selected_brand != 'all' and selected_brand.isdigit():
        products = products.filter(product_brand__id=selected_brand)
    
    if sort_option == 'low-high':
        products = products.order_by('price')
    elif sort_option == 'high-low':
        products = products.order_by('-price')
    elif sort_option == 'a-z':
        products = products.order_by('product_name')
    elif sort_option == 'z-a':
        products = products.order_by('-product_name')
    
    categories = Category.objects.filter(is_deleted=False)
    brands = Brand.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'sort_option': sort_option,
    }
    
    return render(request, 'userside/shop.html', context)


def user_logout(request):
    logout(request)
    return redirect('account:user_home')