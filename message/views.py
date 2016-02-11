from django.shortcuts import render
from .serializers import MessageSerializer
from .models import Message
from rest_framework import viewsets, permissions

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	permission_classes= [permissions.IsAuthenticatedOrReadOnly]
