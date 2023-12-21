from django.urls import path
from . import views


urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('buyer_profile_update/', views.buyer_profile_update,
         name='buyer_profile_update'),
    path('buyer_change_password/', views.buyer_change_password,
         name='buyer_change_password'),
    path('add_favorite/', views.add_favorite,
         name='add_favorite'),
    path('remove_favorite/', views.remove_favorite,
         name='remove_favorite'),


]
