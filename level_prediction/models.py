from django.db import models

class Features(models.Model):
    Age = models.IntegerField()
    Gender = models.CharField(max_length=10)
    Weight = models.FloatField()
    Height = models.FloatField()
    Max_BPM = models.IntegerField()
    Avg_BPM = models.IntegerField()
    Resting_BPM = models.IntegerField()  
    Session_Duration = models.FloatField() 
    Calories_Burned = models.FloatField() 
    Workout_Type = models.CharField(max_length=100)
    Fat_Percentage = models.FloatField() 
    Water_Intake = models.FloatField()  
    Workout_Frequency = models.IntegerField()  
    Experience_Level = models.IntegerField()
    BMI = models.FloatField()  
    def __str__(self):
        return f"Experience Level: {self.Experience_Level}"


class Exercice(models.Model):
    Name = models.CharField(max_length=100)
    Title = models.CharField(max_length=100)
    Excerpt = models.CharField(max_length=100)

    def __str__(self):
        return f"Title: {self.Title}"
