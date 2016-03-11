from rest_framework import serializers
from .models import Post
from user.serializers import UserProfileReadSerializer
from sport.serializers import SportSerializer

class PostReadSerializer(serializers.ModelSerializer):
	author = UserProfileReadSerializer(read_only=True)
	sport = SportSerializer(read_only=True)

	class Meta:
		model = Post
		fields = ('__all__')

class PostCreateUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('sport', 'title', 'description', 'content', 'picture')
