from django.db import models

class Features(models.Model):
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Weight = models.FloatField()
    Height = models.FloatField()
    Max_BPM = models.IntegerField()
    Avg_BPM = models.IntegerField()
    Resting_BPM = models.IntegerField()  # Ajout des parenthèses manquantes
    Session_Duration = models.FloatField()  # Adapté au type float
    Calories_Burned = models.FloatField()  # Adapté au type float
    Workout_Type = models.CharField(max_length=100)
    Fat_Percentage = models.FloatField()  # Adapté au type float
    Water_Intake = models.FloatField()  # Adapté au type float
    Workout_Frequency = models.IntegerField()  # Correction du nom et type
    Experience_Level = models.IntegerField()
    BMI = models.FloatField()  # Adapté au type float

    def __str__(self):
        return f"Experience Level: {self.Experience_Level}"


class Exercice(models.Model):
    Name = models.CharField(max_length=100)
    Title = models.CharField(max_length=100)
    Excerpt = models.CharField(max_length=100)

    def __str__(self):
        return f"Title: {self.Title}"
