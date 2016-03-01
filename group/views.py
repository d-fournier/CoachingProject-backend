from django.shortcuts import render
from .serializers import GroupReadSerializer, GroupCreateSerializer
from .models import Group
from user.models import UserProfile
from message.models import Message
from message.serializers import MessageReadSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

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
			up = UserProfile.objects.get(user=self.request.user)
			queryset = Group.objects.filter(members=up)
		else:
			queryset=Group.objects.none()
		return queryset

	@detail_route(methods=['get'])
	def messages(self,request, pk=None):
		queryset=Message.objects.none()
		group=Group.objects.get(pk=pk)
		if request.user.is_authenticated():
			profile=UserProfile.objects.get(user=request.user)
			if profile in group.members.all():
				queryset=Message.objects.filter(to_group=group).order_by('time')
		serializer=MessageReadSerializer(queryset, many=True)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_200_OK,headers=headers)