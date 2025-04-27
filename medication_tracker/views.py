from django.shortcuts import render, redirect
from django.views import generic
from .models import Medication, SideEffect
from .forms import SideEffectForm

def HomePageView(request):
    return render(request, 'home.html')

class MedicationList(generic.ListView):
    model = Medication
    template_name = 'medication_list.html'
    context_object_name = 'medications'
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Medication.objects.all()
        return Medication.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['side_effect_form'] = SideEffectForm()
        return context

def add_side_effect(request, medication_id):
    if request.method == "POST":
        medication = Medication.objects.get(id=medication_id)
        form = SideEffectForm(request.POST)
        if form.is_valid():
            side_effect = form.save(commit=False)
            side_effect.user = request.user
            side_effect.medication = medication
            side_effect.save()
    return redirect('medication_list')