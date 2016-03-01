from django.shortcuts import render
from .serializers import GroupReadSerializer, GroupCreateSerializer
from .models import Group
from user.models import UserProfile
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	permission_classes= [permissions.DjangoModelPermissionsOrAnonReadOnly]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return GroupReadSerializer
		return GroupCreateSerializer

	def get_queryset(self):	
		if self.request.user.is_superuser:
			queryset = Group.objects.all()	
		elif self.request.user.is_authenticated():
			up = UserProfile(user=self.request.user)
			queryset = Group.objects.filter(users=up)
		else:
			queryset=Group.objects.none()
		return queryset