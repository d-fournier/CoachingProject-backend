from django.shortcuts import render
from .serializers import GroupReadSerializer, GroupCreateSerializer
from .models import Group
from .permissions import GroupPermission
from user.models import UserProfile
from message.models import Message
from message.serializers import MessageReadSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route

# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	permission_classes= [GroupPermission]

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

	@detail_route(methods=['post'])
	def add(self,request, pk=None):
		group=Group.objects.get(pk=pk)
		up = UserProfile.objects.get(user=request.user)
		if up not in group.members.all():
			return Response('You are not in this group, you cannot add people to it', status=status.HTTP_403_FORBIDDEN,headers=headers)
		users = request.data['users']
		for pk in users:
			up = UserProfile.objects.get(pk=pk)
			group.members.add(up)
		serializer = GroupReadSerializer(group)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			sport = serializer.validated_data.get('sport')
			name = serializer.validated_data.get('name')
			description = serializer.validated_data.get('description')
			g = Group(sport=sport,name=name,description=description)
			g.save()
			up = UserProfile.objects.get(user=request.user)
			g.members.add(up)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
