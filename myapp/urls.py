from django.urls import path
from .views import get_products, product_detail, my_products
from .profileView import  create_profile, profile_detail
from .authView import firebase_login

urlpatterns = [
    path('products/', get_products),
    path('products/<int:id>/', product_detail),
    path('profile/', profile_detail),
    path('create-profile/', create_profile),
    path('my-products/', my_products),
    path('firebase-login/', firebase_login),
]