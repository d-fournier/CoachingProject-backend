from rest_framework import serializers
from .models import UserProfile
from level.serializers import LevelSerializer

class UserProfileSerializer(serializers.ModelSerializer):
	levels = LevelSerializer(many=True, read_only=True)

	class Meta:
		model = UserProfile
		fields = ('__all__')