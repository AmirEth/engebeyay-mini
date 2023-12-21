from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from accounts.models import DeliveryCompany, DeliveryGuy, Buyer
from .models import Delivery
from accounts.models import Account
from orders.models import Order, OrderedProduct
from .decorator import delivery_required, verificatoin_required
from django.conf import settings
from django.contrib import messages
# For Delivery Company


@delivery_required
def delivery_dashboard(request):

    return render(request, 'delivery_company/dashboard.html')


@delivery_required
def delivery_details(request):
    user = request.user
    delivery_comp = DeliveryCompany.objects.get(user=user)
    if request.method == 'POST':
        delivery_comp.company_name = request.POST['buissness_name']
        delivery_comp.phone_number = request.POST['phone_number']
        delivery_comp.location = request.POST['location']
        delivery_comp.delivery_fee = request.POST['delivery_fee']
        delivery_comp.save()
        messages.success(request, 'profile Updated successfully.')
        return redirect('delivery_details')
    else:
        context = {'delivery_comp': delivery_comp,
                   'map_api_key': settings.MAP_API_KEY, }
    return render(request, 'delivery_company/detail.html', context)


@delivery_required
def delivery_comp_change_password(request):

    delivery_comp = DeliveryCompany.objects.get(user=request.user)
    if request.POST['password'] == request.POST['confirm_password'] and request.POST['password'] != '':
        # Use set_password to hash the new password
        delivery_comp.user.set_password(request.POST['password'])
        delivery_comp.user.save()  # Save the updated User object
        messages.success(request, 'Password changed successfully.')
        return redirect('login')
    else:
        messages.error(request, 'An error occurred. Please try again.')
        return redirect('delivery_comp_profile')


@verificatoin_required
def delivery_guys(request):

    delivery_providers = DeliveryGuy.objects.all()
    context = {'delivery_providers': delivery_providers}
    return render(request, 'delivery_company/delivery_guys.html', context)


@verificatoin_required
def update_delivery_guy(request, delivery_user):
    delivery = DeliveryGuy.objects.get(user__email=delivery_user)

    if delivery.user.is_active == False:
        delivery.user.is_active = True
        delivery.user.save()
        return redirect('delivery_guys')
    else:
        delivery.user.is_active = False
        delivery.user.save()
        return redirect('delivery_guys')


@verificatoin_required
def add_delivery_guy(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = "delivery"
        username = request.POST.get('first_name'),
        account = Account.objects.create_user(
            email=email, username=username, password=password, is_staff=True, is_active=True)

        DeliveryGuy.objects.create(
            user=account,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone_number=request.POST.get('phone_number'),)
        messages.success(request, 'Delivery guy successfully created.')
        return redirect('add_delivery_guy')
    else:
        return render(request, 'delivery_company/add_delivery_guys.html')


@verificatoin_required
def delivery_orders(request):
    current_user = request.user
    company = DeliveryCompany.objects.get(user=current_user)
    orders = Order.objects.filter(
        delivery_company__user__email=current_user, status="Completed")
    orderditems = OrderedProduct.objects.filter(
        order__delivery_company__user__email=current_user, order__status="Completed")
    delivery_guys = DeliveryGuy.objects.filter(
        company__user__email=current_user, status="Active")
    context = {
        'company': company,
        'orders': orders,
        'orderditems': orderditems,
        'delivery_guys': delivery_guys,
    }
    return render(request, 'delivery_company/delivery_orders.html', context)


@verificatoin_required
def assign_delivery(request):
    if request.method == 'POST':
        form_order = request.POST.get('order')
        order = Order.objects.get(order_number=form_order)
        form_reciver = request.POST.get('reciver')
        reciver = Buyer.objects.get(user__email=form_reciver)
        form_delivery_guy = request.POST.get('delivery_guy')
        delivery_guy = DeliveryGuy.objects.get(user__email=form_delivery_guy)

        Delivery.objects.create(
            order=order,
            reciver=reciver,
            delivery_person=delivery_guy)
        order.status = "Assigned"
        order.save()
        messages.success(request, 'Delivery successfully Assigned!')

    return redirect('delivery_orders')
