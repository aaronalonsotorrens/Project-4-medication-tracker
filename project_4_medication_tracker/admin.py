from django.contrib import admin
from .models import Medication

# Register your models here.
@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'dosage', 'frequency_per_day', 'start_date', 'end_date', 'created_on')
    list_filter = ('start_date', 'end_date')
    ordering = ('-created_on', 'user')
    search_fields = ('name', 'user__username')

    def frequency_per_day(self, obj):
        return f"{obj.frequency} times/day"
    frequency_per_day.short_description = 'Frequency per Day'
