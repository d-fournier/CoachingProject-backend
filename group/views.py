from django.shortcuts import render
from .serializers import GroupReadSerializer, GroupCreateSerializer
from .models import Group, GroupStatus
from .permissions import GroupPermission
from django.core.exceptions import ObjectDoesNotExist
from user.models import UserProfile
from user.serializers import UserProfileReadSerializer
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
		return Group.objects.all()	

	@detail_route(methods=['get'])
	def messages(self,request, pk=None):
		queryset=Message.objects.none()
		group=Group.objects.get(pk=pk)
		if request.user.is_authenticated():
			profile=UserProfile.objects.get(user=request.user)
			if is_user_in_group(profile,group):
				queryset=Message.objects.filter(to_group=group).order_by('time')
		serializer=MessageReadSerializer(queryset, many=True)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_200_OK,headers=headers)

	@detail_route(methods=['post'])
	def add(self,request, pk=None):
		group=Group.objects.get(pk=pk)
		if request.user.is_authenticated :
				if request.data['accepted']:#Demande d'ajout acceptée
					up = UserProfile.objects.get(user=request.user)
					if not is_user_in_group(up,group):
						return Response('You are not in this group, you cannot add people to it', status=status.HTTP_403_FORBIDDEN)
					status_up = GroupStatus.get(group=group,user=up)
					if status_up.status!=GroupStatus.ADMIN:
						return Response('You are not admin of this group, you cannot add people to it', status=status.HTTP_403_FORBIDDEN)
					pk_user = request.data['user']
					try:
						pending_user = UserProfile.objects.get(pk=pk_user)
						status_pending = GroupStatus.get(group=group,user=pending_user)
					except ObjectDoesNotExist:
						return Response('User given is not registered or not in the group', status=status.HTTP_403_FORBIDDEN)
					if status_pending.status==GroupStatus.PENDING:
						status_pending.status=GroupStatus.MEMBER
						status_pending.save()
					return Response('User added to the group with success', status=status.HTTP_200_OK)
				else:#Demande d'ajout refusée
					pk_user = request.data['user']
					try:
						pending_user = UserProfile.objects.get(pk=pk_user)
						status_pending = GroupStatus.get(group=group,user=pending_user)
					except ObjectDoesNotExist:
						return Response('User given is not registered or not in the group', status=status.HTTP_403_FORBIDDEN)
					status_pending.delete()
					return Response('Demand refused', status=status.HTTP_200_OK)
		return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

	@detail_route(methods=['post'])
	def join(self,request, pk=None):
		group=Group.objects.get(pk=pk)
		if(request.user.is_authenticated):
			up = UserProfile.objects.get(user=request.user)
			if is_user_in_group(up,group):
				return Response('You are already in this group', status=status.HTTP_403_FORBIDDEN)
			status_member = GroupStatus(group=group,user=up,status=GroupStatus.PENDING)
			status_member.save()
			return Response('Demand created and sent to the group', status=status.HTTP_201_CREATED)
		return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

	@detail_route(methods=['get'])
	def pending_members(self,request, pk=None):
		group=Group.objects.get(pk=pk)
		status_members = GroupStatus.objects.filter(group=group, status=GroupStatus.PENDING)
		members = []
		for s in status_members:
			members.append(s.user)
		serializer = UserProfileReadSerializer(members, many=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	@detail_route(methods=['get'])
	def members(self,request, pk=None):
		group=Group.objects.get(pk=pk)
		status_members = GroupStatus.objects.filter(group=group)
		members = []
		for s in status_members:
			members.append(s.user)
		serializer = UserProfileReadSerializer(members, many=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	def perform_create(self,serializer):
		up = UserProfile.objects.get(user=self.request.user)
		group = serializer.save()
		status = GroupStatus(group=group,user=up,status=GroupStatus.ADMIN)
		status.save()


def is_user_in_group(user,group):
	try:
		GroupStatus.objects.get(group=group,user=user)
		return True
	except ObjectDoesNotExist :
		return False	