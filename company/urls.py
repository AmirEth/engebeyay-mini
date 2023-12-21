from django.urls import path
from . import views


urlpatterns = [
    path('seller_join/', views.seller_join, name='seller_join'),
    path('delivery_join/', views.delivery_join, name='delivery_join'),
    path('send_message/', views.send_message, name='send_message'),
]
