from django.shortcuts import render
from .serializers import MessageReadSerializer, MessageCreateSerializer
from .models import Message
from user.models import UserProfile
from .permissions import MessagePermission
from rest_framework import viewsets, permissions
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
	permission_classes= [MessagePermission]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return MessageReadSerializer
		return MessageCreateSerializer

	def get_queryset(self):	
		if self.request.user.is_superuser:
			queryset = Message.objects.all()	
		elif self.request.user.is_authenticated():
			queryset = Message.objects.filter(Q(to_relation__coach__user=self.request.user)|Q(to_relation__trainee__user=self.request.user))
		else:
			queryset=Message.objects.none()
		return queryset

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			relation = serializer.validated_data.get('to_relation')
			group = serializer.validated_data.get('to_group')
			if relation is not None and group is not None :
				return Response('You cannot have a relation and a group for the same message, one should be null', status=status.HTTP_400_BAD_REQUEST)
			if relation is not None :
				if relation.requestStatus == True & ((relation.coach.user==request.user) | (relation.trainee.user==request.user)):
					up = UserProfile.objects.get(user=request.user)
					self.object = serializer.save(from_user=up)
					self.object.save()
					headers = self.get_success_headers(serializer.data)
					return Response(serializer.data, status=status.HTTP_201_CREATED,
								headers=headers)
				return Response('Either the relation is not confirmed or you are not involved in it', status=status.HTTP_400_BAD_REQUEST)
			
			if group is not None :
				up = UserProfile.objects.get(user=request.user)
				if up in group.members.all():	
					self.object = serializer.save(from_user=up)
					self.object.save()
					headers = self.get_success_headers(serializer.data)
					return Response(serializer.data, status=status.HTTP_201_CREATED,
								headers=headers)
				return Response('You are not a member of this group', status=status.HTTP_400_BAD_REQUEST)


		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
	def update(self, request, *args, **kwargs):
		instance = self.get_object()
		if instance.to_relation is not None and instance.to_group is not None :
			return Response('You cannot have a relation and a group for the same message, one should be null', status=status.HTTP_400_BAD_REQUEST)
		if instance.to_relation is not None :
			if instance.to_relation.requestStatus == True & ((instance.to_relation.coach.user==request.user) | (instance.to_relation.trainee.user==request.user)):
				if(request.data.get("is_pinned")!= None):
					instance.is_pinned=request.data.get("is_pinned")
					instance.save()			
					serializer = self.get_serializer(instance, data={'is_pinned':request.data.get('is_pinned')}, partial=True)
					serializer.is_valid(raise_exception=True)
					self.perform_update(serializer)
					headers = self.get_success_headers(serializer.data)
					return Response(serializer.data, status=status.HTTP_200_OK,headers=headers)
				return Response('Only the is_pinned value can be modified', status=status.HTTP_400_BAD_REQUEST)	
			return Response('Either the relation is not confirmed or you are not involved in it', status=status.HTTP_400_BAD_REQUEST)
			
		if instance.to_group is not None :
			up = UserProfile.objects.get(user=request.user)
			if up in instance.to_group.members.all():	
				if(request.data.has_key("is_pinned")!=None):
					instance.is_pinned=request.data.get("is_pinned")
					instance.save()			
					serializer = self.get_serializer(instance, data={'is_pinned':request.data.get('is_pinned')}, partial=True)
					serializer.is_valid(raise_exception=True)
					self.perform_update(serializer)
					headers = self.get_success_headers(serializer.data)
					return Response(serializer.data, status=status.HTTP_200_OK,headers=headers)
				return Response('Only the is_pinned value can be modified', status=status.HTTP_400_BAD_REQUEST)	
			return Response('You are not a member of this group', status=status.HTTP_400_BAD_REQUEST)
		return Response('Message need to have either relation or group', status=status.HTTP_400_BAD_REQUEST)
