from django.db import models
from accounts.models import Account, DeliveryCompany
from store.models import Product, Variation


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    # this is the total amount paid
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Completed', 'Completed'),
        ('Assigned', 'Assigned'),
        ('Delivred', 'Delivred'),
    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=20)
    reciver_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
  #  delivery_company = models.ForeignKey(
   #     DeliveryCompany, on_delete=models.SET_NULL, null=True,)
    ip = models.CharField(blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_added = models.DateField(auto_now_add=True,  null=True)
  #  latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
   # longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    is_qr_emailed = models.BooleanField(default=False)

    def __str__(self):
        return self.order_number


class OrderedProduct(models.Model):

    STATUS = (
        ('Waiting', 'Waiting'),
        ('Paid', 'Paid'),

    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seller_status = models.CharField(
        max_length=10, choices=STATUS, default='Waiting')

    def __str__(self):
        return self.product.product_name


class Refund(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_payment = models.FloatField()
    is_payed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)
