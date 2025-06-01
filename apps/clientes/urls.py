from django.urls import path
from .views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView
)


urlpatterns = [
    path('clients/', ClientListView.as_view(), name='clients'),
    path('add/', ClientCreateView.as_view(), name='add_client'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
]
