from django.urls import path
from . import views
from .views import QuickAssignmentView

from .views import AssignLockerView

urlpatterns = [
    path('', views.quick_assignment, name='quick_assignment'),
    path('lockers/', views.lockers, name='lockers'),
    path('locker/add/', views.add_locker, name='add_locker'),
    path('locker/update/<int:pk>', views.update_locker, name='update_locker'),
    path('locker/delete/<int:pk>', views.delete_locker, name='delete_locker'),
     path('locker/assign/<int:pk>/', AssignLockerView.as_view(), name='assign_locker'),
    path('cards/', views.cards, name='cards'),
    path('card/add/', views.add_card, name='add_card'),
    path('card/update/<int:pk>', views.update_card, name='update_card'),
    path('card/delete/<int:pk>', views.delete_card, name='delete_card'),
    path('quick-assignment/', QuickAssignmentView.as_view(), name='quick_assignment'),
]
