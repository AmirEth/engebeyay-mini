from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from orders.models import Order, OrderedProduct, Refund
from store.models import Product
from carts.models import Favorite
from accounts.models import Buyer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import redirect, render
from django.contrib import messages
from .decorator import buyer_required

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
# Create your views here.


@buyer_required
def dashboard(request):
    current_user = request.user
    orders = Order.objects.filter(user=current_user, status="Completed")
    orderditems = OrderedProduct.objects.filter(
        user=current_user, order__status="Completed")
    got_orderditems = OrderedProduct.objects.filter(
        user=current_user, order__status="Delivred")
    context = {
        'orders': orders,
        'orderditems': orderditems,
        'got_orderditems': got_orderditems,
    }
    return render(request, 'accounts/dashboard.html', context)


@buyer_required
def cancel_order(request):
    current_user = request.user
    if request.method == 'POST':
        Refund.objects.create(
            user=current_user, total_payment=request.POST.get('order_total')
        )
        order_num = request.POST.get('order_num')
        order = Order.objects.get(order_number=order_num)
        order.delete()
        # send email about order cancellation
        # Send an email notification to the user
        subject = 'Order Cancellation Confirmation'
        message = f"Dear {current_user.username},\n\nYour order with number {order_num} has been canceled.\n and we will contact you shortly to return 75% of your refund in few hours\nThank you."
        from_email = settings.EMAIL_HOST_USER
        to_email = current_user.email

        send_mail(subject, message, from_email, [to_email])
        messages.success(request, 'Order Cancelled successfully.')
        return redirect('dashboard')
    else:
        messages.error(request, 'An error occurred. Please try again!')
        return redirect('dashboard')


@buyer_required
def buyer_profile_update(request):
    buyer = Buyer.objects.get(user=request.user)
    if request.method == 'POST':
        buyer.first_name = request.POST['first_name']
        buyer.last_name = request.POST['last_name']
        buyer.phone_number = request.POST['phone_number']
        buyer.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('dashboard')
    else:
        messages.error(request, 'An error occurred. Please try again!')
        return redirect('dashboard')


@buyer_required
def buyer_change_password(request):
    buyer = Buyer.objects.get(user=request.user)
    if request.POST['password'] == request.POST['confirm_password'] and request.POST['password'] != '':
        # Use set_password to hash the new password
        buyer.user.set_password(request.POST['password'])
        buyer.user.save()  # Save the updated User object
        messages.success(request, 'Password changed successfully.')
        return redirect('login')
    else:
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('dashboard')


@buyer_required
def add_favorite(request):
    current_user = request.user
    product = Product.objects.get(product_id=request.POST['product'])
    if request.method == 'POST':
        Favorite.objects.create(
            user=current_user, product=product)

    return redirect('store')


@buyer_required
def remove_favorite(request):
    product_id = request.POST['product']
    current_user = request.user
    fov = Favorite.objects.get(
        product__product_id=product_id, user=current_user)
    fov.delete()

    return redirect('store')
