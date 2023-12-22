from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from store.models import Product
from category.models import Category
from accounts.models import Seller, Buyer, Staff, DeliveryCompany, Account
from company.models import Company_Information, Payment_Method, Message
from orders.models import OrderedProduct, Order, Refund
from .decorator import staff_required
from django.conf import settings
import requests
from django.contrib import messages
from requests.exceptions import RequestException, ConnectionError


# Create your views here.


@staff_required
def admin_dashboard(request):

    products = Product.objects.all()
    order = Order.objects.all()

    order_count = order.count()
    order_revenue = Order.objects.all().aggregate(Sum('order_total'))
    order_total = order_revenue.get('order_total__sum')
    if order_total is None:
        company_revenue = 0
        order_total = "0"
    else:
        # company revenue is 1.5% of all the sales
        company_revenue = order_total*0.015

    total_buyer = Buyer.objects.count()
    total_seller = Seller.objects.count()
    total_users = total_buyer+total_seller

    context = {'total_order': order_count, 'products': products,
               'products': products, 'sales': order_total, 'revenue': company_revenue, 'total_users': total_users}

    return render(request, 'admin/admin_dashboard.html', context)


@staff_required
def admin_profile(request):
    staff = Staff.objects.get(user=request.user)
    if request.method == 'POST':
        staff.first_name = request.POST['first_name']
        staff.last_name = request.POST['last_name']
        staff.phone_number = request.POST['phone_number']
        staff.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('admin_profile')
    else:
        return render(request, 'admin/admin_profile.html', {'staff': staff})


@staff_required
def change_password(request):
    staff = Staff.objects.get(user=request.user)
    if request.POST['password'] == request.POST['confirm_password']:
        staff.user.password = make_password(request.POST['password'])
        staff.save()
        messages.success(request, 'Password Changed successfully.')
        return redirect('login')
    else:
        return render(request, 'admin/admin_profile.html', {'staff': staff})


@staff_required
def admin_product_items(request):
    products = Product.objects.all()
    context = {'products': products, }

    return render(request, 'admin/product/all_items.html', context)


@staff_required
def admin_product_delete(request, product_id):

    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('admin_product_items')


@staff_required
def admin_product_category(request):
    if request.method == 'POST':

        cat = Category.objects.create(
            category_name=request.POST['category_name'],
            slug=request.POST['slug'],
            description=request.POST['description']),
        messages.success(request, 'Catagory added successfully.')
        return redirect('admin_product_category')

    else:
        Categories = Category.objects.all()
        context = {'Categories': Categories, }
        return render(request, 'admin/product/add_category.html', context)


@staff_required
# Staff
def admin_user_staff(request):

    # if email exist handle error!
    if request.method == 'POST':
       # Added on users
        email = request.POST.get('email')
        password = "staff"
        username = request.POST.get('first_name'),
        account = Account.objects.create_user(
            email=email, username=username, password=password, is_staff=True, is_active=True, is_verified=True)
        # Added on staff
        Staff.objects.create(
            user=account,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            phone_number=request.POST.get('phone_number'),)
        return redirect('admin_user_staff')
    else:
        staffs = Staff.objects.all()
        context = {'staffs': staffs}
        return render(request, 'admin/users/staff.html', context)


@staff_required
def update_staff(request, staff_user):
    staff = Staff.objects.get(user__email=staff_user)

    if staff.user.is_active == False:
        staff.user.is_active = True
        staff.user.save()
        return redirect('admin_user_staff')
    else:
        staff.user.is_active = False
        staff.user.save()
        return redirect('admin_user_staff')


@staff_required
# buyer
def admin_user_buyer(request):
    buyers = Buyer.objects.all()
    context = {'buyers': buyers, }
    return render(request, 'admin/users/buyer.html', context)

# block/Activate_Buyer


@staff_required
def update_buyer(request, buyer_user):
    buyer = Buyer.objects.get(user__email=buyer_user)

    if buyer.user.is_active == False:
        buyer.user.is_active = True
        buyer.user.save()
        return redirect('admin_user_buyer')
    else:
        buyer.user.is_active = False
        buyer.user.save()
        return redirect('admin_user_buyer')


@staff_required
def admin_user_seller(request):
    sellers = Seller.objects.all()
    context = {'sellers': sellers, }

    return render(request, 'admin/users/seller.html', context)


@staff_required
def update_seller(request, seller_user):
    seller = Seller.objects.get(user__email=seller_user)

    if seller.user.is_active == False:
        seller.user.is_active = True
        seller.user.save()
        return redirect('admin_user_seller')
    else:
        seller.user.is_active = False
        seller.user.save()
        return redirect('admin_user_seller')


@staff_required
def admin_user_delivery(request):
    deliverys = DeliveryCompany.objects.all()
    context = {'deliverys': deliverys, }

    return render(request, 'admin/users/delivery_providers.html', context)


@staff_required
def update_delivery(request, delivery_user):
    delivery = delivery.objects.get(user__email=delivery_user)

    if delivery.user.is_active == False:
        delivery.user.is_active = True
        delivery.user.save()
        return redirect('admin_user_delivery')
    else:
        delivery.user.is_active = False
        delivery.user.save()
        return redirect('admin_user_delivery')


@staff_required
def admin_transaction(request):
    orders = OrderedProduct.objects.filter(
        order__status="Delivred", seller_status="Waiting")
    ordered_items = orders.values(
        'order__order_number', 'product__owner__user__email', 'product__owner__merchant_id', 'order__ip').annotate(total_order_amount=Sum('product_price'))

    context = {'ordered_items': ordered_items}
    return render(request, 'admin/transaction.html', context)


@staff_required
def unverified_users(request):
    users = Account.objects.filter(is_verified=False,is_seller=True)

    context = {'users': users}
    return render(request, 'admin/unverified_users.html', context)


@staff_required
def admin_companyDetails(request):
    user = request.user
    company = Company_Information.objects.get(current_admin=user)
    api_key = settings.MAP_API_KEY
    context = {'company': company,
               "map_api_key": api_key, }
    return render(request, 'admin/company.html', context)


@staff_required
def admin_companypayments(request):
    if request.method == 'POST':

        Payment_Method.objects.create(
            payment_method=request.POST.get('method'),
            payment_provider=request.POST.get('provider'),
            currency=request.POST.get('currency'),
            merchant_id=request.POST.get('merchant_id'),)
        messages.success(request, 'Payment Created successfully.')
        return redirect('admin_companypayments')
    else:

        payment = Payment_Method.objects.all()
        context = {'payments': payment, }
        return render(request, 'admin/payments.html', context)


def remove_companypayments(request, payment):

    payment = Payment_Method.objects.get(payment_method=payment)
    payment.delete()

    return redirect('admin_companypayments')


@staff_required
def admin_refund(request):
    refund = Refund.objects.filter(is_payed=False)
    context = {'refunds': refund}
    return render(request, 'admin/refund.html', context)


def remove_refund(request, pk):
    refund = Refund.objects.get(pk=pk)
    refund.delete()

    return redirect('admin_refund')


def confirm_unverified_user(request, user):

    person = Account.objects.get(email=user)
    person.is_verified = True
    person.save()

    return redirect('un_verified_users')


def feedbacks(request):
    messages = Message.objects.filter(message_type="feedback")
    return render(request, 'company/feedback.html', {'messages': messages})


# Pay sellers

def admin_pay_sellers(request):
    try:
        ii = request.GET.get('itemName')
        total = request.GET.get('TotalAmount')
        moi = request.GET.get('MerchantOrderId')
        ti = request.GET.get('TransactionId')
        status = request.GET.get('Status')
        url = 'https://testapi.yenepay.com/'
        datax = {
            "requestType": "PDT",
            "pdtToken": "Q1woj27RY1EBsm",
            "transactionId": ti,
            "merchantOrderId": moi
        }

        x = requests.post(url, datax)

        if x.status_code == 200:
            values = moi.split('Q')
            order_number = values[0]
            email = values[1] if len(values) > 1 else None
            ordered_products = OrderedProduct.objects.filter(
                order__order_number=order_number, product__owner__user__email=email)
            print(moi)
            for ordered_product in ordered_products:
                ordered_product.seller_status = "Paid"
                ordered_product.save()

            messages.success(request, 'Seller is Paid Sucessfuly.')
            return redirect('admin_transaction')
        else:
            messages.error(request, 'Invalid Payment Process.')
            return redirect('admin_transaction')

    except ConnectionError:
        # Handle the connection error gracefully
        return render(request, 'admin/connection_error.html')

    except RequestException:
        # Handle other request-related exceptions
        return render(request, 'admin/connection_error.html')


# backup database
