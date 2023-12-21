from django.urls import path
from . import views


urlpatterns = [

    path('seller_register/', views.Seller_register.as_view(), name='seller_register'),
    path('login/', views.login_user, name='login'),

    path('buyer_register/', views.Buyer_register.as_view(), name='buyer_register'),
    path('delivery_register/', views.Delivery_register.as_view(),
         name='delivery_register'),

    path('logout/', views.logout, name='logout'),


    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',
         views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('purchase_detail/', views.purchase_detail, name='purchase_detail'),
]
