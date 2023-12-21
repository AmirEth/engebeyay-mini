from django.urls import path
from . import views

urlpatterns = [

    path('delivery_dashboard/', views.delivery_dashboard,
         name='delivery_dashboard'),
    path('delivery_details/', views.delivery_details, name='delivery_details'),
    path('delivery_guys/', views.delivery_guys, name='delivery_guys'),
    path('update_delivery_guy/<str:delivery_user>/', views.update_delivery_guy,
         name='update_delivery_guy'),
    path('delivery_comp_change_password/', views.delivery_comp_change_password,
         name='delivery_comp_change_password'),
    path('add-delivery_guy/', views.add_delivery_guy, name='add_delivery_guy'),
    path('delivery_orders/', views.delivery_orders, name='delivery_orders'),
    path('assign_delivery/', views.assign_delivery, name='assign_delivery'),



]
