from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout 
from django.contrib import messages
from account.models import User
from utils.admindecorator import admin_required




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