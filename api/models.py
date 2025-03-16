from django.db import models

class LupusData(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    fever = models.CharField(max_length=10,default="No")  
    alopecia = models.CharField(max_length=10,default="No")  
    oral_ulcers = models.CharField(max_length=10,default="No")  
    discoidRash = models.CharField(max_length=10,default="No")   
    photosensitivity = models.CharField(max_length=10,default="No")  
    jointPain = models.CharField(max_length=10,default="No")  
    pleuralEffusion = models.CharField(max_length=10,default="No")  
    pericarditis = models.CharField(max_length=10,default="No")   
    delirium = models.CharField(max_length=10,default="No")   
    psychosis = models.CharField(max_length=10,default="No")  
    seizure = models.CharField(max_length=10,default="No")  
    renalClass2 = models.CharField(max_length=10,default="No")  
    renalClass3 = models.CharField(max_length=10,default="No")  
    anticardiolipin = models.CharField(max_length=10,default="No")  
    antiB2GPI = models.CharField(max_length=10,default="No")  
    lupusAnticoagulant = models.CharField(max_length=10,default="No")  

    urine_routine = models.FloatField(blank=True, null=True)
    haemoglobin = models.FloatField(blank=True, null=True)
    tlc = models.FloatField(blank=True, null=True)
    platelet_count = models.FloatField(blank=True, null=True)
    c3 = models.FloatField(blank=True, null=True)
    c4 = models.FloatField(blank=True, null=True)
    antiDsDNA = models.FloatField(blank=True, null=True) 
    antiSmith = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Lupus Data {self.id}"
