from django.urls import path
from . import views

urlpatterns = [
    path('', views.quick_assignment, name='quick-assignment'),
    path('register-card/', views.register_card, name='register-card'),
]