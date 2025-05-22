from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Medication, SideEffect
from .forms import MedicationForm, SideEffectForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection
from django.shortcuts import render

def HomePageView(request):
    return render(request, 'medications/index.html')

class MedicationList(generic.ListView):
    model = Medication
    template_name = 'medications/medication_list.html'
    context_object_name = 'medications'
    paginate_by = 6

    def get_queryset(self):
        # Admins see all, others see only their meds
        queryset = Medication.objects.all() if self.request.user.is_superuser else Medication.objects.filter(user=self.request.user)

        # Optional: improve query efficiency by including user info
        queryset = queryset.select_related('user')

        # Sorting logic
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'user' and self.request.user.is_superuser:
            queryset = queryset.order_by('user__username')
        elif sort_by == 'date_created':
            queryset = queryset.order_by('created_on')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['side_effect_form'] = SideEffectForm()


        # Include side effects grouped by medication for logged-in user
        user_side_effects = SideEffect.objects.filter(user=self.request.user)
        effects_by_med = {}
        for effect in user_side_effects:
            if effect.medication.id not in effects_by_med:
                effects_by_med[effect.medication.id] = []
            effects_by_med[effect.medication.id].append(effect)

        context['side_effects_by_med'] = effects_by_med
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
            messages.success(request, "✅ Side effect reported successfully.")
        else:
            messages.error(request, "There was an error reporting the side effect.")
    return redirect('medication_list')


class SideEffectDelete(LoginRequiredMixin, DeleteView):
    model = SideEffect
    template_name = 'medications/side_effect_confirm_delete.html'
    success_url = reverse_lazy('medication_list')

    def get_queryset(self):
        # Ensure that users can only delete their own side effects
        return SideEffect.objects.filter(user=self.request.user)
    

class MedicationCreate(LoginRequiredMixin, CreateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'medications/medication_form.html'
    success_url = reverse_lazy('medication_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class MedicationUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Medication
    form_class = MedicationForm
    template_name = 'medications/medication_form.html'
    success_url = reverse_lazy('medication_list')

    def test_func(self):
        medication = self.get_object()
        return self.request.user == medication.user or self.request.user.is_superuser
    

class MedicationDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Medication
    template_name = 'medications/medication_confirm_delete.html'
    success_url = reverse_lazy('medication_list')

    def test_func(self):
        medication = self.get_object()
        return self.request.user == medication.user or self.request.user.is_superuser
    
@staff_member_required
def admin_dashboard(request):
    # We'll prepare data for all genders found + 'All'
    genders = ['Male', 'Female', 'Other']  # Adjust based on your data

    with connection.cursor() as cursor:
        # Total medications and side effects
        cursor.execute("SELECT COUNT(*) FROM medications_medication;")
        total_meds = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM medications_sideeffect;")
        total_side_effects = cursor.fetchone()[0]

        # Medications by category (all)
        cursor.execute("""
            SELECT category, COUNT(*) 
            FROM medications_medication
            GROUP BY category
            ORDER BY COUNT(*) DESC
        """)
        all_meds = cursor.fetchall()

        # Side effects by category (all)
        cursor.execute("""
            SELECT category, COUNT(*) 
            FROM medications_sideeffect
            GROUP BY category
            ORDER BY COUNT(*) DESC
        """)
        all_side_effects = cursor.fetchall()

        # Build medication data dict with gender keys
        gender_medication_data = {
            "All": {
                "labels": [row[0] for row in all_meds],
                "counts": [row[1] for row in all_meds],
            }
        }

        # Build side effect data dict with gender keys
        gender_side_effect_data = {
            "All": {
                "labels": [row[0] for row in all_side_effects],
                "counts": [row[1] for row in all_side_effects],
            }
        }

        # Fetch gender-specific data for meds and side effects
        for gender in genders:
            # Medications filtered by gender
            cursor.execute("""
                SELECT m.category, COUNT(*) 
                FROM medications_medication m
                JOIN auth_user u ON m.user_id = u.id
                JOIN accounts_userprofile up ON u.id = up.user_id
                WHERE up.gender = %s
                GROUP BY m.category
                ORDER BY COUNT(*) DESC
            """, [gender])
            med_gender_data = cursor.fetchall()
            gender_medication_data[gender] = {
                "labels": [row[0] for row in med_gender_data],
                "counts": [row[1] for row in med_gender_data],
            }

            # Side effects filtered by gender
            cursor.execute("""
                SELECT se.category, COUNT(*) 
                FROM medications_sideeffect se
                JOIN auth_user u ON se.user_id = u.id
                JOIN accounts_userprofile up ON u.id = up.user_id
                WHERE up.gender = %s
                GROUP BY se.category
                ORDER BY COUNT(*) DESC
            """, [gender])
            se_gender_data = cursor.fetchall()
            gender_side_effect_data[gender] = {
                "labels": [row[0] for row in se_gender_data],
                "counts": [row[1] for row in se_gender_data],
            }

    context = {
        "total_meds": total_meds,
        "total_side_effects": total_side_effects,
        "gender_medication_data": gender_medication_data,
        "gender_side_effect_data": gender_side_effect_data,
        "genders": ["All"] + genders,
        "selected_gender": request.GET.get('gender', 'All'),
    }

    return render(request, 'medications/admin_dashboard.html', context)