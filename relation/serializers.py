from rest_framework import serializers
from .models import Relation
from user.serializers import UserProfileReadSerializer
from sport.serializers import SportSerializer

class RelationReadSerializer(serializers.ModelSerializer):
	coach = UserProfileReadSerializer(read_only=True)
	trainee = UserProfileReadSerializer(read_only=True)
	sport = SportSerializer(read_only=True)

	class Meta:
		model = Relation
		fields = ('__all__')

class RelationCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Relation
		fields = ('id','coach','sport','comment')

class RelationUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Relation
		fields = ('requestStatus','active')



		