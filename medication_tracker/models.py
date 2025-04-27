from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.IntegerField(help_text="Times per day")
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    

class SideEffect(models.Model):
    medication = models.ForeignKey(Medication, related_name='side_effects', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    reported_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Side effect for {self.medication.name} by {self.user.username}"