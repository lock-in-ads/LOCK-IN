from django.urls import path
from . import views

urlpatterns = [  
    path('clients/', views.clients, name='clients'),     
    path('client/add/', views.add_client, name='add_client'), 
    path('client/update/<int:pk>', views.update_client, name='update_client'),
    path('client/delete/<int:pk>', views.delete_client, name='delete_client'),
]