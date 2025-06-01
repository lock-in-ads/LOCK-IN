from django.urls import path
import apps.administrativo.views as views
from .views import (
    QuickAssignmentView,
    AssignLockerView,
    ListLockersView,
    AddLockerView,
    UpdateLockerView,
    DeleteLockerView
)


urlpatterns = [
    path('', QuickAssignmentView.as_view(), name='quick_assignment'),
    path('lockers/', ListLockersView.as_view(), name='lockers'),
    path('locker/add/', AddLockerView.as_view(), name='add_locker'),
    path(
        'locker/update/<int:pk>/',
        UpdateLockerView.as_view(),
        name='update_locker'
    ),
    path(
        'locker/delete/<int:pk>/',
        DeleteLockerView.as_view(),
        name='delete_locker'
    ),
    path(
        'locker/assign/<int:pk>/',
        AssignLockerView.as_view(),
        name='assign_locker'
    ),
    path('cards/', views.cards, name='cards'),
    path('card/add/', views.add_card, name='add_card'),
    path('card/update/<int:pk>/', views.update_card, name='update_card'),
    path('card/delete/<int:pk>/', views.delete_card, name='delete_card'),
]
