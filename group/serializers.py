from rest_framework import serializers
from .models import Group
from user.serializers import UserProfileReadSerializer
from sport.serializers import SportSerializer

class GroupReadSerializer(serializers.ModelSerializer):
	members = UserProfileReadSerializer(many=True,read_only=True)
	sport = SportSerializer(read_only=True)
	
	class Meta:
		model = Group
		fields = ('__all__')

class GroupCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('name','description','sport','city','private')