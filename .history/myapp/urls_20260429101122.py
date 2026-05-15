from django.urls import path
from .views import get_students

urlpatterns = [
    path('students/', get_students),
    path('students/<int:id>/', get_students),
]