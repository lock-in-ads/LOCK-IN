from django.urls import path
from . import views

urlpatterns = [
    path('', views.quick_assignment, name='quick_assignment'),    
    path('lockers/', views.list_lockers, name='lockers'),  
    path('locker/add/', views.add_locker, name='add_locker'),
    #path('locker/update/<int:id>', views.update_locker, name='update-locker'),
    #path('locker/delete/<int:id>', views.delete_locker, name='delete-locker'),
    path('locker/assign/<int:id>', views.assign_locker, name='assign_locker'),

    path('card/add/', views.add_card, name='add_card'),    
    
    path('users/', views.users, name='users'),     
    path('user/add/', views.add_user, name='add_user'), 
]