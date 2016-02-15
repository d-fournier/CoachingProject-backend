from django.shortcuts import render
from .serializers import MessageSerializer
from .models import Message
from rest_framework import viewsets, permissions
from django.db.models import Q

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
	serializer_class = MessageSerializer
	permission_classes= [permissions.IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		queryset = Message.objects.filter(Q(to_relation__coach__user=self.request.user)|Q(to_relation__trainee__user=self.request.user))
		return queryset
        
