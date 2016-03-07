from django.shortcuts import render
from .serializers import MessageReadSerializer, MessageCreateSerializer, MessageUpdateSerializer
from .models import Message
from user.models import UserProfile
from device import scripts
from .permissions import MessagePermission
from rest_framework import viewsets, permissions
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
	permission_classes= [MessagePermission]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return MessageReadSerializer
		elif self.action=='partial_update':
			return MessageUpdateSerializer
		return MessageCreateSerializer

	def get_queryset(self):	
		if self.request.user.is_superuser:
			queryset = Message.objects.all()	
		elif self.request.user.is_authenticated():
			queryset = Message.objects.filter(Q(to_relation__coach__user=self.request.user)|Q(to_relation__trainee__user=self.request.user))
		else:
			queryset=Message.objects.none()
		return queryset

	def perform_create(self,serializer):
		data = serializer.validated_data
		up = UserProfile.objects.get(user=self.request.user)
		users = []
		relation, group = serializer.validated_data.get('to_relation'), serializer.validated_data.get('to_group')
		if relation is not None and group is not None :
			raise ValidationError('You cannot have a relation and a group for the same message, one should be null')
		if relation is not None :
			if relation.requestStatus!=True :
				raise ValidationError('You cannot send a message because the relation is not confirmed')
			if relation.coach!=up and relation.trainee!=up:
				raise ValidationError('You cannot send a message because you are not involved in this relation')
			users.append(relation.trainee if relation.coach==up else relation.coach)
		if group is not None :
			if up not in group.members.all():
				raise ValidationError('You cannot send a message because you are not a member of this group')
			users.append(group.members.all())
			users.remove(up)		
		m = serializer.save(from_user=up)
		scripts.sendGCMNewMessage(users=users,message=m)
		

	def perform_update(self,serializer):
		data = serializer.validated_data
		up = UserProfile.objects.get(user=self.request.user)
		message = serializer.instance
		relation, group = message.to_relation, message.to_group
		if relation is not None and relation.coach!=up and relation.trainee!=up :
			raise ValidationError('You cannot update this message because you are not involved in this relation')
		if group is not None and up not in group.members.all():
			raise ValidationError('You cannot update this message because you are not a member of this group')
		serializer.save()