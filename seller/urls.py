from django.urls import path
from . import views


urlpatterns = [
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller_profile/', views.seller_profile, name='seller_profile'),
    path('seller_change_password/', views.seller_change_password,
         name='seller_change_password'),
    path('seller_items/', views.seller_items, name='seller_items'),
    path('add-item/', views.addItem, name='add_item'),
    path('update_item/<str:pk>/', views.update_item, name='update_item'),
    path('delete_item/<str:pk>/', views.delete_item, name='delete_item'),
    path('orders/', views.orders, name='orders'),

]
