from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medication(models.Model):
    HEALTH_CATEGORIES = [
        ('joints', 'Joints and Muscles'),
        ('gut', 'Gut Health'),
        ('skin', 'Skin'),
        ('ent', 'Eyes-Ears-Nose-Throat'),
        ('neuro', 'Headaches and Dizziness'),
        ('cardio', 'Heart Health'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.IntegerField(help_text="Times per day")
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.CharField(max_length=20, choices=HEALTH_CATEGORIES)
    notes = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    

class SideEffect(models.Model):
    SIDE_EFFECT_CATEGORIES = [
        ('nausea', 'Nausea or Vomiting'),
        ('fatigue', 'Fatigue or Weakness'),
        ('rash', 'Rashes or Skin Issues'),
        ('mood', 'Mood Changes'),
        ('pain', 'Muscle or Joint Pain'),
        ('cardio', 'Heart Palpitations or Chest Pain'),
    ]
    medication = models.ForeignKey(Medication, related_name='side_effects', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=SIDE_EFFECT_CATEGORIES)
    description = models.TextField()
    reported_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Side effect for {self.medication.name} by {self.user.username}"