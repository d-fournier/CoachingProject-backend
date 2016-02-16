from django.shortcuts import render
from .serializers import LevelReadSerializer, LevelCreateSerializer
from .models import Level
from rest_framework import viewsets, permissions

# Create your views here.
class LevelViewSet(viewsets.ModelViewSet):
	queryset = Level.objects.all()
	permission_classes= [permissions.IsAuthenticatedOrReadOnly]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return LevelReadSerializer
		return LevelCreateSerializer
