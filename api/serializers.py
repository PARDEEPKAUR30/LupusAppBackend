from rest_framework import serializers
from .models import LupusData

class LupusDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LupusData
        fields = '__all__'
