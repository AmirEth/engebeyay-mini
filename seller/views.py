from django.shortcuts import render
from accounts.models import Seller
from store.models import Product
from .forms import AddProductForm
from django.shortcuts import redirect
from orders.models import Order, OrderedProduct
from store.models import Product
from category.models import Category
from .decorator import seller_required, verificatoin_required
from django.contrib import messages


@seller_required
def seller_dashboard(request):

    return render(request, 'seller/seller_dashboard.html',)


@seller_required
def seller_profile(request):
    seller = Seller.objects.get(user=request.user)
    if request.method == 'POST':
        seller.buisness_name = request.POST['buisness_name']
        seller.merchant_id = request.POST['merchant_id']
        seller.phone_number = request.POST['phone_number']
        seller.latitude = request.POST['latitude']
        seller.longitude = request.POST['longitude']
        seller.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('seller_profile')
    else:
        return render(request, 'seller/seller_profile.html', {'seller': seller})


@seller_required
def seller_change_password(request):
    seller = Seller.objects.get(user=request.user)
    if request.POST['password'] == request.POST['confirm_password'] and request.POST['password'] != '':
        # Use set_password to hash the new password
        seller.user.set_password(request.POST['password'])
        seller.user.save()  # Save the updated User object
        messages.success(request, 'Password changed successfully.')
        return redirect('login')
    else:
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('seller_profile')


@verificatoin_required
def seller_items(request):
    seller = Seller.objects.get(user=request.user)
    products = Product.objects.filter(owner=seller)
    totalproducts = Product.objects.filter(owner=seller).count()
    context = {'products': products, 'totalproducts': totalproducts}

    return render(request, 'seller/seller_items.html', context)


@verificatoin_required
def addItem(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        # form = AddProductForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form = form.save(commit=False)
        #     form.owner = request.user
        #     form.save()
        #     return redirect('seller')
        owner = request.user.seller

        product_name = request.POST['product_name']
        product_id = product_name
        slug = product_name
        description = request.POST['description']
        price = request.POST['price']
        images = request.FILES.get('image')

        stock = request.POST['stock']
        category = request.POST.get('category')
        selected = Category.objects.get(category_name=category)

        new_product = Product(owner=owner, product_id=product_id, product_name=product_name,
                              slug=slug, description=description, price=price, stock=stock, category=selected,

                              images=images)
        new_product.save()
        messages.success(request, 'Product added Sucessfuly.')
        return redirect('seller_items')

    context = {'categories': categories}
    return render(request, 'seller/add_items.html', context)


@verificatoin_required
def update_item(request, pk):
    product = Product.objects.get(id=pk)
    category = Category.objects.get(category_name=product.category)
    ex_cat = Category.objects.exclude(category_name=product.category)
    categories = ex_cat.all()

    if request.method == 'POST':
        product.owner = request.user.seller
        product.product_name = request.POST['product_name']
        product.product_id = product.product_name
        product.slug = product.product_name
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.images = product.images

        product.stock = request.POST['stock']
        category = request.POST.get('category')
        product.category = Category.objects.get(category_name=category)
        product.save()
        messages.success(request, 'Product Updated Sucessfuly.')
        return redirect('seller_items')
    context = {'product': product,
               'categories': categories, 'category': category}

    return render(request, 'seller/update_item.html', context)


@verificatoin_required
def delete_item(request, pk):
    product = Product.objects.get(id=pk)
    # if request.method == 'POST':
    #     confirm = request.POST.get('confirm', '')
    #     if confirm == 'yes':
    product.delete()
    return redirect('seller_dashboard')

    # context = {'product': product}

    # return render(request, 'seller/seller_items.html', context)


@verificatoin_required
def orders(request):
    seller = Seller.objects.get(user=request.user)
    ordered_items = OrderedProduct.objects.filter(
        product__owner=seller, order__status="Completed")

    context = {'ordered_items': ordered_items}
    return render(request, 'seller/orders.html', context)
