from rest_framework import serializers
from .models import Message
from user.serializers import UserProfileReadSerializer
from relation.serializers import RelationReadSerializer
from group.serializers import GroupReadSerializer


class MessageReadSerializer(serializers.ModelSerializer):
	from_user = UserProfileReadSerializer(read_only=True)
	to_relation = RelationReadSerializer(read_only=True)
	to_group = GroupReadSerializer(read_only=True)

	class Meta:
		model = Message
		fields = ('__all__')

class MessageCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('to_relation', 'to_group', 'content')

class MessageUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Message
		fields = ('is_pinned')