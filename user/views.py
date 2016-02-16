from django.shortcuts import render
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import viewsets, permissions

# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
	serializer_class = UserProfileSerializer
	permission_classes= [permissions.IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		queryset = UserProfile.objects.all()
		keywords = self.request.query_params.get('keywords', None)
		if keywords is not None :
			queryset = queryset.filter(displayName__iexact=keywords)|queryset.filter(description__contains=keywords)
		coach = self.request.query_params.get('coach', None)
		if coach is not None :
			queryset = queryset.filter(isCoach=coach)
		sport = self.request.query_params.get('sport', None)
		if sport is not None :
			queryset = queryset.filter(levels__sport__id=sport)
		return queryset
