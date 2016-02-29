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
			if relation.requestStatus == True & ((relation.coach.user==request.user) | (relation.trainee.user==request.user)):
				up = UserProfile.objects.get(user=request.user)
				self.object = serializer.save(from_user=up)
				self.object.save()
				headers = self.get_success_headers(serializer.data)
				return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
			return Response('Either the relation is not confirmed or you are not involved in it', status=status.HTTP_400_BAD_REQUEST)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
