from rest_framework import serializers
from .models import UserProfile
from level.serializers import LevelReadSerializer

class UserProfileReadSerializer(serializers.ModelSerializer):
	levels = LevelReadSerializer(many=True, read_only=True)

	class Meta:
		model = UserProfile
		fields = ('__all__')

class UserProfileCreateSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = UserProfile
		fields = ('__all__')