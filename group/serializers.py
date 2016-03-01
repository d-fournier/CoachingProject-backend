from rest_framework import serializers
from .models import Group
from user.serializers import UserProfileReadSerializer

class GroupReadSerializer(serializers.ModelSerializer):
	users = UserProfileReadSerializer(many=True,read_only=True)
	
	class Meta:
		model = Group
		fields = ('__all__')

class GroupCreateSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Group
		fields = ('__all__')