from django.urls import path
from . import views
urlpatterns=[
    path('',views.shop_login),
    path('logout',views.shop_logout),
    path('register',views.register),

# ------------------Admin--------------------------------

    path('shop_home',views.shop_home),
    path('add_product',views.add_product),
    path('edit_pro/<id>',views.edit_pro),
    path('delete_pro/<id>',views.delete_pro),
    path('bookings',views.bookings),

    
#------------------user----------------------------------
    path('user_home',views.user_home),
    path('view_pro/<id>',views.view_pro),
    path('add_to_cart/<id>',views.add_to_cart),
    path('cart_display',views.cart_display),
    path('delete_cart/<id>',views.delete_cart),
    path('buy_pro/<id>',views.buy_pro),
    path('user_view_bookings',views.user_view_bookings),
]