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
		username = self.request.query_params.get('username', None)
		if username is not None :
			queryset = queryset.filter(user__username=username)
		coach = self.request.query_params.get('isCoach', False)
		queryset = queryset.filter(isCoach=coach)
		return queryset
