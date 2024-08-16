from django.shortcuts import render,redirect
from .models import Brand
from utils.admindecorator import admin_required


# Create your views here.
@admin_required
def brand_create(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        description = request.POST.get('description', '')
        brand_image = request.FILES.get('brand_image')
        brand_status = request.POST.get('status') == 'on'
        
        if brand_name and brand_image:
            brand = Brand.objects.create(
                brand_name=brand_name,  
                brand_image=brand_image, 
                description=description,
                status=brand_status 
            )
            
            brand.save()
            return redirect('brand:brand_list') 
    return render(request, 'brand/brand_create.html')

@admin_required
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brand/brand.html', {'brands': brands})
