from django.shortcuts import render
from django.views import generic
from .models import Medication

# Create your views here.

class MedicationList (generic.ListView):
    model = Medication
    template_name = "medication_tracker.html"
