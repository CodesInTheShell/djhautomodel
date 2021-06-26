from rest_framework import serializers
from .models import AutoMLModel

class AutomlSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoMLModel
        fields = "__all__"