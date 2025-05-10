from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Medication(models.Model):
    HEALTH_CATEGORIES = [
        ('Joints', 'Joints and Muscles'),
        ('Gut', 'Gut Health'),
        ('Skin', 'Skin'),
        ('Sensory', 'Eyes-Ears-Nose-Throat'),
        ('Neuro', 'Headaches and Dizziness'),
        ('Cardio', 'Heart Health'),
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
        ('Nausea', 'Nausea or Vomiting'),
        ('Fatigue', 'Fatigue or Weakness'),
        ('Rash', 'Rashes or Skin Issues'),
        ('Mood', 'Mood Changes'),
        ('Pain', 'Muscle or Joint Pain'),
        ('Cardio', 'Heart Palpitations or Chest Pain'),
    ]
    medication = models.ForeignKey(Medication, related_name='side_effects', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=SIDE_EFFECT_CATEGORIES)
    description = models.TextField()
    reported_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Side effect for {self.medication.name} by {self.user.username}"