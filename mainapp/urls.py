from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path("shop/", views.shop, name="shop"),                        # default -> Office Basics
    path("shop/category/<slug:slug>/", views.shop, name="shop_by_category"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Auth
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),


    path('my-order/', views.my_order, name='my_order'),
    path('track-order/', views.track_order, name='track_order'),

    # Cart
    path("cart/", views.cart_view, name="cart_view"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/buy/<int:product_id>/", views.buy_now, name="buy_now"),
    path("cart/update/", views.update_cart, name="update_cart"),
    path("cart/remove/", views.remove_cart_item, name="remove_cart_item"),



    # Checkout + Orders
    path("checkout/", views.checkout, name="checkout"),
    path("order/success/<int:order_id>/", views.order_success, name="order_success"),
    path("my-order/", views.my_order, name="my_order"),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),

]
