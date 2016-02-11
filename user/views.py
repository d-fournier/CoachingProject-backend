from django.shortcuts import render
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import viewsets, permissions

# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
	queryset = UserProfile.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes= [permissions.IsAuthenticatedOrReadOnly]


class CoachsViewSet(viewsets.ModelViewSet):
	queryset = UserProfile.objects.filter(isCoach=True)
	serializer_class = UserProfileSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
