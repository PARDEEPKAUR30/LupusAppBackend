from django.db import models

class LupusData(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    fever = models.BooleanField(default=False)  
    alopecia = models.BooleanField(default=False)
    oral_ulcers = models.BooleanField(default=False)
    discoidRash = models.BooleanField(default=False) 
    photosensitivity = models.BooleanField(default=False)
    jointPain = models.BooleanField(default=False)
    pleuralEffusion = models.BooleanField(default=False)
    pericarditis = models.BooleanField(default=False) 
    delirium = models.BooleanField(default=False) 
    psychosis = models.BooleanField(default=False)
    seizure = models.BooleanField(default=False)
    renalClass2 = models.BooleanField(default=False)
    renalClass3 = models.BooleanField(default=False)
    anticardiolipin = models.BooleanField(default=False)
    antiB2GPI = models.BooleanField(default=False) 
    lupusAnticoagulant = models.BooleanField(default=False)

    urine_routine = models.FloatField()
    haemoglobin = models.FloatField()
    tlc = models.FloatField()
    platelet_count = models.FloatField()
    c3 = models.FloatField()
    c4 = models.FloatField()
    antiDsDNA = models.FloatField() 
    antiSmith = models.FloatField()

    def __str__(self):
        return f"Lupus Data {self.id} - Fever: {self.fever}"
