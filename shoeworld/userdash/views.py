from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .models import UserAddress
from account.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.

# @login_required(login_url='/user_login/')
# def userdash(request):
#     return render(request,'userside/user_dash.html')

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
    return render(request, 'userside/user_dash.html', {
        'user_address': user_address,
        'user_data': user_data,
        'user': user,
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
        user.email = request.POST.get('email')
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
