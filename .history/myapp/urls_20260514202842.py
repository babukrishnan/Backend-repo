from django.urls import path
from .views import get_products, product_detail
from .profileView import  create_profile, profile_detail
from .authView import send_otp, verify_otp

urlpatterns = [
    path('products/', get_products),
    path('products/<int:id>/', product_detail),
    path('profile/', profile_detail),
    path('create-profile/', create_profile),
    path('send-otp/', send_otp),
    path('verify-otp/', verify_otp),
    path('my-products/', my_products),
]