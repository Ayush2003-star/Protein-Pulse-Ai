from django.db import models

# Create your models here.

class ProteinData(models.Model):
    

    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    weight_kg= models.CharField(max_length=100)
    activity_level= models.CharField(max_length=100)
    purpose= models.CharField(max_length=100)
    lean_body_mass_kg= models.CharField(max_length=100)
    bmr= models.CharField(max_length=100)
    protein_need_per_lean_kg_sedentary= models.CharField(max_length=100)
    protein_need_per_lean_kg_active= models.CharField(max_length=100)
    protein_need_per_lean_kg_very_active= models.CharField(max_length=100)
    protein_per_kg_min= models.CharField(max_length=100)
    protein_per_kg_moderate= models.CharField(max_length=100)
    protein_per_kg_max= models.CharField(max_length=100)
    activity_protein_multiplier= models.CharField(max_length=100)
    adjusted_protein_need= models.CharField(max_length=100)
    age_protein_factor= models.CharField(max_length=100)
    protein_for_age_group= models.CharField(max_length=100)
    gender_protein_base= models.CharField(max_length=100)
    protein_gender_adjusted= models.CharField(max_length=100)
    purpose_protein_multiplier= models.CharField(max_length=100)
    protein_for_purpose= models.CharField(max_length=100)
    lean_to_total_ratio= models.CharField(max_length=100)
    muscle_mass_score= models.CharField(max_length=100)
    bmr_per_kg= models.CharField(max_length=100)
    protein_metabolic_need= models.CharField(max_length=100)
    training_intensity= models.CharField(max_length=100)
    recovery_protein_need= models.CharField(max_length=100)
    protein_g= models.CharField(max_length=100)
    
    
    
    
    
class ProteiDataHist(models.Model):
      Age = models.CharField(max_length=100)
      Gender = models.CharField(max_length=100)
      Height_cm = models.CharField(max_length=100)
      Weight_kg = models.CharField(max_length=100)
      Activity_Level = models.CharField(max_length=100)
      Fitness_Goal = models.CharField(max_length=100)
      Meals_Per_Day = models.CharField(max_length=100)
      FitnessExperience = models.CharField(max_length=100)
      protein_g         = models.CharField(max_length=100)