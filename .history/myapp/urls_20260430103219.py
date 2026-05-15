from django.urls import path
from .views import get_students, student_detail

urlpatterns = [
    path('students', get_students),
    path('students/<int:id>/', student_detail),
]