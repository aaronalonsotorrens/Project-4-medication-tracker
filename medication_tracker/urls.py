from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView, name='home'),
    path('medications/', views.MedicationList.as_view(), name='medication_list'),
    path('medications/<int:medication_id>/add-side-effect/', views.add_side_effect, name='add_side_effect'),
]