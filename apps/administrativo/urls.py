from django.urls import path
from . import views

urlpatterns = [
    path('', views.quick_assignment, name='quick_assignment'),    
    path('lockers/', views.lockers, name='lockers'),  
    path('locker/add/', views.add_locker, name='add_locker'),
    path('locker/update/<int:pk>', views.update_locker, name='update_locker'),
    path('locker/delete/<int:pk>', views.delete_locker, name='delete_locker'),
    path('locker/assign/<int:pk>', views.assign_locker, name='assign_locker'),

    path('cards/', views.cards, name='cards'),
    path('card/add/', views.add_card, name='add_card'),   
]