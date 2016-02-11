from django.shortcuts import render
from .serializers import LevelSerializer
from .models import Level
from rest_framework import viewsets, permissions

# Create your views here.
class LevelViewSet(viewsets.ModelViewSet):
	queryset = Level.objects.all()
	serializer_class = LevelSerializer
	permission_classes= [permissions.DjangoModelPermissions]
