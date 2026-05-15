from django.urls import path
from .views import get_products, product_detail
from .profileView import profile_detail

urlpatterns = [
    path('products/', get_products),
    path('products/<int:id>/', product_detail),
    path('profile/',profile_detail),
]