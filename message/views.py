from django.shortcuts import render
from .serializers import MessageSerializer
from .models import Message
from rest_framework import viewsets, permissions
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
	serializer_class = MessageSerializer
	permission_classes= [permissions.IsAuthenticatedOrReadOnly]

	def get_queryset(self):		
		if self.request.user.is_authenticated():
			queryset = Message.objects.filter(Q(to_relation__coach__user=self.request.user)|Q(to_relation__trainee__user=self.request.user))
		else:
			queryset=Message.objects.none()
		return queryset

	def create(self,request):
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():

			relation = serializer.validated_data.get('to_relation')
			if relation.requestStatus == True & ((relation.coach.user==self.request.user) | (relation.trainee.user==self.request.user)):
				self.object = serializer.save()
				self.object.save()
				headers = self.get_success_headers(serializer.data)
				return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
			return Response('Relation not accessible', status=status.HTTP_400_BAD_REQUEST)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
