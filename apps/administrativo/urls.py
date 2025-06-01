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

from .views import (
    CardListView,
    CardUpdateView,
    CardDeleteView,
    CardAddView
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
    path('cards/', CardListView.as_view(), name='cards'),
    path('card/add/', CardAddView.as_view(), name='add_card'),
    path('card/update/<int:pk>/', CardUpdateView.as_view(), name='update_card'),
    path('card/delete/<int:pk>/', CardDeleteView.as_view(), name='delete_card'),
]
