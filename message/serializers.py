from rest_framework import serializers
from .models import Message
from user.serializers import UserProfileSerializer
from relation.serializers import RelationSerializer

class MessageSerializer(serializers.ModelSerializer):
	from_user = UserProfileSerializer(read_only=True)
	to_relation = RelationSerializer(read_only=True)

	class Meta:
		model = Message
		fields = ('__all__')