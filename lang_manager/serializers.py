from rest_framework import serializers
from .models import Language

class LanguageSerializer(serializers.ModelSerializer):  # Still relevant
    class Meta:
        model = Language
        fields = ['id', 'code', 'name', 'is_active']
