from django.contrib import admin
from .models import Medication, SideEffect

# Register your models here.
@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'dosage', 'frequency_per_day', 'start_date', 'end_date', 'created_on')


    def frequency_per_day(self, obj):
        return f"{obj.frequency} times/day"
    frequency_per_day.short_description = 'Frequency per Day'

@admin.register(SideEffect)
class SideEffectAdmin(admin.ModelAdmin):
    list_display = ('medication', 'user', 'description', 'reported_on')
    search_fields = ('medication__name', 'user__username', 'description')
    list_filter = ('medication', 'user')