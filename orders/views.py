from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderedProduct
from accounts.models import DeliveryCompany
from company.models import Payment_Method
import json
from store.models import Product, Variation
from requests.exceptions import RequestException, ConnectionError
# send Qr code to the user's email
import qrcode
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO

import requests
from geopy.geocoders import Nominatim
from django.template.loader import render_to_string
from buyer.decorator import buyer_required


@buyer_required
def place_order(request, total=0, quantity=0,):
    current_user = request.user

    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
      # Tax for all the orderd items: 15%
    tax = (15 * total)/100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.reciver_name = form.cleaned_data['reciver_name']
            data.phone = form.cleaned_data['phone']
            #data.latitude = request.POST.get('latitude')
            #data.longitude = request.POST.get('longitude')
            #delivery = request.POST.get('delivery')
            #data.delivery_company = DeliveryCompany.objects.get(
             #   user__email=delivery)
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            hr = int(datetime.datetime.now().strftime('%H'))
            mn = int(datetime.datetime.now().strftime('%M'))
            current_time = hr + mn
            current_date_time = current_date + str(current_time)
            order_number = current_date_time + data.reciver_name
            data.order_number = order_number
            checkdata = Order.objects.all()
            if checkdata.filter(user=current_user, status="New").exists():
                print("data already exists")
            else:
                data.save()
            order = Order.objects.get(
                user=current_user, status="New")
            company_payment = Payment_Method.objects.get(
                payment_method="YenePay")
            merchant_id = company_payment.merchant_id
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'merchant_id': merchant_id
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


@buyer_required
def order_complete(request):
    #try:
        current_user = request.user
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
            print(f"YenePay API Response: Status Code {x.status_code}, Content: {x.text}")
            data = Payment(user=current_user, payment_id=ti,
                           payment_method="Yenepay", status=status, amount_paid=total)

            # Unfortunetly YenePay donot have way to send diffrent transaction Id so we can use the code below
            # checkdata = Payment.objects.all()
            # if checkdata.filter(user=current_user, payment_id=ti,
            #                   payment_method="Yenepay", status="Paid", amount_paid=total).exists():
            #  print("data already exists")
            # else:

            data.save()
            order = Order.objects.get(user=request.user, order_number=moi)
            order.status = "Completed"
            order.save()
            # save payment data to the database

            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                try:
                    ordered_product = OrderedProduct.objects.get(
                        order=order, product=item.product)
                    # If an OrderedProduct already exists for the current item, update the quantity
                    ordered_product.quantity += item.quantity
                    ordered_product.save()
                except OrderedProduct.DoesNotExist:
                    # If no OrderedProduct exists, create a new one
                    ordered_product = OrderedProduct(
                        order=order,
                        user=request.user,
                        payment=data,
                        product=item.product,
                        quantity=item.quantity,
                        product_price=item.product.price
                    )
                    ordered_product.save()

                try:
                    # variation = Variation.objects.get(product__product_id=item.product, attribute='Color: Blue')
                    # ordered_product.variations.add(variation)
                    variations = Variation.objects.filter(
                        product__product_id=item.product)
                    for variation in variations:
                        ordered_product.variations.add(variation.id)
                except Variation.DoesNotExist:
                    print("Product has no variation")

                # Reduce the quantity of the sold products
                try:
                    product = Product.objects.get(product_id=item.product)
                    product.stock -= item.quantity
                    product.save()
                except Product.DoesNotExist:
                    print("Product not found")
            # Clear cart
            CartItem.objects.filter(user=request.user).delete()
            orderd_items = OrderedProduct.objects.filter(
                order__order_number=moi)

            # Send the unique Qr to the buyer's email for delivery!
            subject = 'Your Order QR Code'
            message = 'Thank you for choosing to shop on Engebeyay. Please find the QR code for your order attached.'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [current_user.email]
            email = EmailMessage(
                subject,
                message,
                email_from,
                recipient_list,
            )
            # generate Qr code
            qr = qrcode.QRCode(
                version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=4)
            qr.add_data(order.order_number)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            if not order.is_qr_emailed:
                # Attach the QR code image to the email
                img_name = f'order_{order.order_number}_qr.png'
                img_io = BytesIO()
                img.save(img_io, format='PNG')
                img_file = ContentFile(img_io.getvalue())
                email.attach(img_name, img_file.read(), 'image/png')
                # set is_qr_emailed to True
                order.is_qr_emailed = True
                order.save()
                # send the email
                email.send()
            else:
                # the email has already been sent
                print('email sent!')
            # total item price
            items_price = order.order_total-order.tax

            # delivery location
            dest_latitude = None
            dest_longitude = None
            #dest_latitude = order.latitude
            #dest_longitude = order.longitude
           # geolocator = Nominatim(user_agent="Engebeyay")

            #location = geolocator.reverse(
             #   f"{dest_latitude}, {dest_longitude}", addressdetails=True)
            #city = location.raw['address'].get('city', '')

            context = {'total': total,
                       'status': status,
                       'transactionId': ti,
                       'order': order,
                       'items_price': items_price,
                       'orderd_items': orderd_items,
                    #   'city': city

                       }
            return render(request, 'orders/order_complete.html', context)
        else:
            print('Invalid payment process')
            return render(request, 'orders/order_cancelled.html')
  #  except ConnectionError:
        # Handle the connection error gracefully
   #     return render(request, 'orders/connection_error.html')

    #except RequestException:
        # Handle other request-related exceptions
     #   return render(request, 'orders/connection_error.html')


@buyer_required
def order_cancelled(request):
    return render(request, 'orders/order_cancelled.html.html')
