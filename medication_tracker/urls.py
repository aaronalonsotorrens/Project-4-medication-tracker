from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView, name='home'),
    path('medications/', views.MedicationList.as_view(), name='medication_list'),
    path('medications_create/', views.MedicationCreate.as_view(), name='medication_create'),
    path('medications/<int:pk>/edit/', views.MedicationUpdate.as_view(), name='medication_update'),
    path('medications/<int:pk>/delete/', views.MedicationDelete.as_view(), name='medication_delete'),
    path('medications/<int:medication_id>/add-side-effect/', views.add_side_effect, name='add_side_effect'),
    path('side-effects/<int:pk>/delete/', views.SideEffectDelete.as_view(), name='side_effect_delete'),
]