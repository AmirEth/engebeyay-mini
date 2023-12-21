from django.db import models
from accounts.models import Buyer, DeliveryGuy
from orders.models import Order
# Create your models here.


class Delivery(models.Model):
    STATUS = (
        ('Recived', 'Recived'),
        ('InProgress', 'InProgress'),
        ('Completed', 'Completed'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    reciver = models.ForeignKey(
        Buyer, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=15, choices=STATUS, default='Recived')
    delivery_person = models.ForeignKey(
        DeliveryGuy, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_added = models.DateField(auto_now_add=True,  null=True)

    def __str__(self):
        return str(self.order)
