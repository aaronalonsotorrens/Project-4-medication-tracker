from django.shortcuts import render
from django.views import generic
from .models import Medication

# Create your views here.

class MedicationList(generic.ListView):
    queryset = Medication.objects.all()
    template_name = "medication_tracker/index.html"
    paginate_by = 6
