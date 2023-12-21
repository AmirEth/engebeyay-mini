from django.urls import path
from . import views


urlpatterns = [
    # Profile and Pass
    path('admin/', views.admin_dashboard, name='admin'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('admin_change_pass/', views.change_password, name='change_password'),

    # items and category
    path('admin_product-items/', views.admin_product_items,
         name='admin_product_items'),
    path('admin_product-delete/<int:product_id>/', views.admin_product_delete,
         name='admin_product_delete'),
    path('admin_product-category/', views.admin_product_category,
         name='admin_product_category'),
    path('admin_companyDetails/', views.admin_companyDetails,
         name='admin_companyDetails'),
    path('admin_companypayments/', views.admin_companypayments,
         name='admin_companypayments'),

    path('remove_companypayments/<str:payment>/', views.remove_companypayments,
         name='remove_companypayments'),
    path('remove_refund/<int:pk>/', views.remove_refund,
         name='remove_refund'),
    path('feedbacks/', views.feedbacks, name='feedbacks'),



    # View and block Users of Engebeyay
    # Staff
    path('admin_user-staff/', views.admin_user_staff,
         name='admin_user_staff'),
    path('update_staff/<str:staff_user>/',
         views.update_staff, name='update_staff'),

    # Buyer
    path('admin_user-buyer/', views.admin_user_buyer,
         name='admin_user_buyer'),
    path('update_buyer/<str:buyer_user>/',
         views.update_buyer, name='update_buyer'),

    # Seller
    path('admin_user-seller/', views.admin_user_seller,
         name='admin_user_seller'),
    path('update_seller/<str:seller_user>/',
         views.update_seller, name='update_seller'),

    # Delivery
    path('admin_user-delivery/', views.admin_user_delivery,
         name='admin_user_delivery'),
    path('update_delivery/<str:delivery_user>/',
         views.update_delivery, name='update_delivery'),

    # Report and Transaction
    path('admin_transaction/', views.admin_transaction,
         name='admin_transaction'),

    path('admin_refund/', views.admin_refund,
         name='admin_refund'),

    path('un-verified_users/', views.unverified_users,
         name='un_verified_users'),
    path('confirm_unverified_user/<str:user>/',
         views.confirm_unverified_user, name='confirm_unverified_user'),

    # backup database and pay sellers
    path('admin_pay_sellers/', views.admin_pay_sellers,
         name='admin_pay_sellers'),
]
