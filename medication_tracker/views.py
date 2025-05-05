from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Medication, SideEffect
from .forms import MedicationForm, SideEffectForm

def HomePageView(request):
    return render(request, 'medication_tracker/index.html')

class MedicationList(generic.ListView):
    model = Medication
    template_name = 'medication_tracker/medication_list.html'
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


class MedicationCreate(LoginRequiredMixin, CreateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'medication_tracker/medication_form.html'
    success_url = reverse_lazy('medication_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class MedicationUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'medication_tracker/medication_form.html'
    success_url = reverse_lazy('medication_list')

    def test_func(self):
        medication = self.get_object()
        return self.request.user == medication.user or self.request.user.is_superuser
    

class MedicationDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Medication
    template_name = 'medication_tracker/medication_confirm_delete.html'
    success_url = reverse_lazy('medication_list')

    def test_func(self):
        medication = self.get_object()
        return self.request.user == medication.user or self.request.user.is_superuser