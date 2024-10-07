from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from product.models import  *
from categoryy.models import Category
from brand.models import Brand
from utils.admindecorator import admin_required
from django.contrib.auth.decorators import login_required



@admin_required
def product_create(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_description = request.POST.get('product_description')
        product_brand_id = request.POST.get('product_brand')
        product_category_id = request.POST.get('product_category')
        price = request.POST.get('price')
        offer_price = request.POST.get('offer_price')
        status = request.POST.get('is_active') == 'on'
        thumbnail = request.FILES.get('thumbnail') 

        
        try:
            product_brand = Brand.objects.get(id=product_brand_id) if product_brand_id else None
        except Brand.DoesNotExist:
            messages.error(request, "Selected brand does not exist.")
            return redirect('product:product_create')
        
        try:
            product_category = Category.objects.get(id=product_category_id) if product_category_id else None
        except Category.DoesNotExist:
            messages.error(request, "Selected category does not exist.")
            return redirect('product:product_create')
        
        product = Products.objects.create(
            product_name=product_name,
            product_description=product_description,
            product_category=product_category,
            product_brand=product_brand,
            price=price,
            offer_price=offer_price,
            is_active=status,
            thumbnail = thumbnail

        )

        product.save()
        return redirect('product:product_view')

    else:
        categories = Category.objects.all()
        brands = Brand.objects.all()
    return render(request, 'product/product_create.html', {'categories': categories, 'brands': brands})
    

@admin_required
def product_view(request):
    products = Products.objects.all().order_by('id')
    return render(request, 'product/product.html', {'products': products})


@admin_required
def product_info(request, pk):
    product = get_object_or_404(Products, id=pk)
    images = ProductImages.objects.filter(product=product)
    variants = ProductVariant.objects.filter(product=product)
    return render(request, 'product/product_info.html', {'product': product, 'images': images, 'variants': variants})


def product_delete(request, pk):
    product = get_object_or_404(Products, id=pk)
    product.is_active = not product.is_active
    product.save()
    return redirect('product:product_view')


@admin_required
def product_edit(request, pk):
    # Fetch all categories and brands for dropdowns
    categories = Category.objects.all()
    brands = Brand.objects.all()
    # Get the product instance
    product = get_object_or_404(Products, id=pk)

    # If the request method is POST, update the product details
    if request.method == 'POST':
        # Update the product instance with the data from the form
        product.product_name = request.POST.get('product_name')
        product.product_description = request.POST.get('product_description')
        product_category_id = request.POST.get('product_category')
        product_brand_id = request.POST.get('product_brand')
        product.price = request.POST.get('price')
        product.offer_price = request.POST.get('offer_price')
        if request.FILES.get('thumbnail'):
            product.thumbnail = request.FILES['thumbnail'] 
        product.is_active = 'is_active' in request.POST 


        # Update the product's category and brand if provided
        product.product_category = get_object_or_404(Category, id=product_category_id) if product_category_id else None
        product.product_brand = get_object_or_404(Brand, id=product_brand_id) if product_brand_id else None
  
        # Save the updated product instance
        product.save()
        
        # Redirect to the product list page
        return redirect('product:product_view')
    else:
        # If the request method is GET, render the edit product template
        return render(request, 'product/product_edit.html', {'product': product, 'categories': categories, 'brands': brands})



@admin_required
def product_image(request, pk):
    product = get_object_or_404(Products, id=pk)
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        
        for image in images:
            ProductImages.objects.create(product=product, images=image)
        
        return redirect('product:product_view')
    
    return render(request, 'product/product_image.html', {'product': product})


@admin_required
def delete_image(request, pk):
    image = get_object_or_404(ProductImages, id=pk)
    product_id = image.product.id
    image.delete()
    return redirect('product:product_info', pk=product_id)

@admin_required
def variants_view(request, pk):
    product = get_object_or_404(Products, id=pk)
    variants = ProductVariant.objects.filter(product=product)
    return render(request, 'product/product_variant.html', {'product': product, 'variants': variants})

@admin_required
def variant_create(request, pk):
    product = get_object_or_404(Products, pk=pk)
    
    if request.method == 'POST':
        size = request.POST.get('size')
        variant_stock = request.POST.get('variant_stock')
        variant_status = request.POST.get('variant_status') == 'on'
        
        # Check if a variant with the same size already exists for the product
        if ProductVariant.objects.filter(product=product, size=size).exists():
            messages.error(request, 'A variant with this size already exists for this product.')
        else:
            ProductVariant.objects.create(
                product=product,
                size=size,
                variant_stock=variant_stock,   
                variant_status=variant_status,
            )
            return redirect('product:product_view')
    
    return render(request, 'product/create_variant.html', {'product': product})

@admin_required
def variant_edit(request, pk):
    variant = get_object_or_404(ProductVariant, id=pk)
    product = variant.product

    if request.method == 'POST':
        size = request.POST.get('size')
        variant_stock = request.POST.get('variant_stock')
        variant_status = request.POST.get('variant_status') == 'on'

        # Check if another variant with the new size already exists for the product
        if ProductVariant.objects.filter(product=product, size=size).exclude(id=pk).exists():
            messages.error(request, 'A variant with this size already exists for this product.')
            return render(request, 'product/edit_variant.html', {'variant': variant})
        
        variant.size = size
        variant.variant_stock = variant_stock
        variant.variant_status = variant_status
        variant.save()

        return redirect('product:product_variant', pk=product.id)
    else:
        return render(request, 'product/edit_variant.html', {'variant': variant})


@admin_required
def variant_status(request, pk):
    variant = get_object_or_404(ProductVariant, id=pk)
    product_id = variant.product.id
    variant.variant_status = not variant.variant_status
    variant.save()
    return redirect('product:product_variant', pk=product_id)

        # ---------------------------------review-----------------------------------
@login_required(login_url="/user_login/")
def review_create(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            product = get_object_or_404(Products, pk=pk)
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            
            if comment=="":
                messages.error(request, 'Please write comment.')
                return redirect('account:single_product', pk=pk)
            if rating is None or rating == '0':
                messages.error(request, 'Please select a star rating.')
                return redirect('account:single_product', pk=pk)

            # Creating and saving the review
            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                comment=comment
            )
            review.save()

            return redirect('account:single_product', pk=pk)
        else:
            # Redirect to login page if user is not authenticated
            return redirect('account:user_login')
    else:
        return redirect('account:single_product', pk=pk)
    
    



@login_required(login_url="/user_login/")
def delete_review(request, pk):
    # Fetch the review by primary key
    review = get_object_or_404(Review, id=pk)
    
    # Handle POST request to delete the review
    if request.method == 'POST':
        # Check if the logged-in user is the owner of the review
        if request.user.is_authenticated and request.user == review.user:
            product_id = review.product.id
            review.delete()  # Delete the review
            return redirect('account:single_product', pk=product_id)
        else:
            # Redirect to product details if the user is not authorized
            messages.error(request, 'You can not delete this review.')
            return redirect('account:single_product', pk=review.product.id)
    
    # Redirect if the request method is not POST
    return redirect('account:single_product', pk=review.product.id)