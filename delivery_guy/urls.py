from django.urls import path
from . import views

urlpatterns = [
    # Delivery Person
    path('assiged_delivery/', views.assiged_delivery, name='assiged_delivery'),
    path('current_delivery/', views.current_delivery, name='current_delivery'),
    path('delivery_profile/', views.delivery_profile, name='delivery_profile'),
    path('confirm_delivery/',
         views.confirm_delivery, name='confirm_delivery'),
    path('delivery_change_pass/', views.delivery_guy_change_password,
         name='delivery_guy_change_password'),
]
