"""fashionjet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page,name='login'),
    path('logout/', views.signout,name='logout'),
    path('register/', views.register_page,name='register'),
    path('activate/<email_token>/', views.activate_email,name='register'),
    path('add-to-cart/<uid>/',views.add_to_cart,name='add_to_cart'),
    path('cart/',views.cart,name='cart'),
    path('remove-cart/<cart_item_uid>/',views.remove_cart,name='remove_cart'),
    path('remove-coupon/<cart_uid>/',views.remove_coupon,name='remove_coupon'),
    path('success/',views.success,name='success'),
    path('invoice/',views.invoice,name='invoice'),
]