from rest_framework import serializers
from .models import Level
from sport.serializers import SportSerializer

class LevelReadSerializer(serializers.ModelSerializer):
	sport = SportSerializer(read_only=True)
	
	class Meta:
		model = Level
		fields = ('__all__')

class LevelCreateSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Level
		fields = ('__all__')