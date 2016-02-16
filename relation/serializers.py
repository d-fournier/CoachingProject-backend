from rest_framework import serializers
from .models import Relation
from user.serializers import UserProfileSerializer
from sport.serializers import SportSerializer

class RelationSerializer(serializers.ModelSerializer):
	coach = UserProfileSerializer(read_only=True)
	trainee = UserProfileSerializer(read_only=True)
	sport = SportSerializer(read_only=True)

	class Meta:
		model = Relation
		fields = ('__all__')