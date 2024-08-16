from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import CategoryForm
from utils.admindecorator import admin_required

@admin_required
def list_category(request):
    categories = Category.objects.all().order_by('id')
    return render(request, 'adminside/category.html', {'categories':categories})
    
@admin_required
def create_category(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('category:list_category')

    return render(request, 'adminside/create_category.html', {'form':form})


@admin_required
def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category:list_category')  
    else:
        form = CategoryForm(instance=category)
    return render(request, 'adminside/edit_category.html', {'form': form, 'category': category})

@admin_required
def delete_category(request, pk):
    delete_category = get_object_or_404(Category, id=pk)
    delete_category.is_deleted = not delete_category.is_deleted
    delete_category.save()
    return redirect('category:list_category') 