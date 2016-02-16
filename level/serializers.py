from rest_framework import serializers
from .models import Level
from sport.serializers import SportSerializer

class LevelSerializer(serializers.ModelSerializer):
	sport = SportSerializer(read_only=True)
	
	class Meta:
		model = Level
		fields = ('__all__')