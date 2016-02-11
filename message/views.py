from django.shortcuts import render
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import viewsets, permissions

# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	permission_classes= [permissions.IsAuthenticatedOrReadOnly]
