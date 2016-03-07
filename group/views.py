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
	permission_classes= [GroupPermission]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return GroupReadSerializer
		return GroupCreateSerializer

	def get_queryset(self):	
		return Group.objects.filter(private=False)	

	@detail_route(methods=['get'])
	def messages(self,request, pk=None):
		if request.user.is_authenticated():
			up=UserProfile.objects.get(user=request.user)
			group=Group.objects.get(pk=pk)
			if is_user_in_group(up,group):
				queryset=Message.objects.filter(to_group=group).order_by('time')
			else:
				return Response('You are not a member of the group', status=status.HTTP_403_FORBIDDEN)

		else:
			return Response('You are not connected', status=status.HTTP_403_FORBIDDEN)
		serializer=MessageReadSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	@detail_route(methods=['post'])
	def add(self,request, pk=None):
		if request.user.is_authenticated() :
			up=UserProfile.objects.get(user=request.user)
			group=Group.objects.get(pk=pk)
			if is_user_admin_in_group(up,group):
				pending_users_id = request.data['users']
				for pk_user in pending_users_id:
					try:
						pending_user = UserProfile.objects.get(pk=pk_user)
						pending_user_group_status = GroupStatus.get(group=group,user=pending_user)
					except ObjectDoesNotExist:
						return Response('User given is not registered or not in the group', status=status.HTTP_400_BAD_REQUEST)
					if request.data['accepted']:#Demande d'ajout acceptée
						if pending_user_group_status.status==GroupStatus.PENDING:
							pending_user_group_status.status=GroupStatus.MEMBER
							pending_user_group_status.save()
							return Response('User added to the group with success', status=status.HTTP_200_OK)
						else:
							return Response('User given is already in the group', status=status.HTTP_400_BAD_REQUEST)
					else:#Demande d'ajout refusée
						pending_user_group_status.delete()
						return Response('Demand from user refused', status=status.HTTP_200_OK)
			else:
				return Response('You are not admin of this group', status=status.HTTP_403_FORBIDDEN)		
		return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

	@detail_route(methods=['post'])
	def join(self,request, pk=None):
		if request.user.is_authenticated() :
			group=Group.objects.get(pk=pk)
			if group.private:
				return Response('This group is private', status=status.HTTP_403_FORBIDDEN)
			up = UserProfile.objects.get(user=request.user)
			if is_user_in_group(up,group):
				return Response('You are already in this group', status=status.HTTP_403_FORBIDDEN)
			status_member = GroupStatus(group=group,user=up,status=GroupStatus.PENDING)
			status_member.save()
			return Response('Demand created and sent to the group', status=status.HTTP_201_CREATED)
		return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

	@detail_route(methods=['get'])
	def pending_members(self,request, pk=None):
		if request.user.is_authenticated() :
			group=Group.objects.get(pk=pk)
			up = UserProfile.objects.get(user=request.user)
			if is_user_admin_in_group(up,group):
				status_members = GroupStatus.objects.filter(group=group, status=GroupStatus.PENDING)
				members = []
				for s in status_members:
					members.append(s.user)
				serializer = UserProfileReadSerializer(members, many=True)
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response('You are not admin of this group', status=status.HTTP_403_FORBIDDEN)
		else:
			return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)
		

	@detail_route(methods=['get'])
	def members(self,request, pk=None):
		if request.user.is_authenticated() :
			group=Group.objects.get(pk=pk)
			if group.private:
				return Response('This group is private', status=status.HTTP_403_FORBIDDEN)
			status_members = GroupStatus.objects.filter(group=group)
			members = []
			for s in status_members:
				members.append(s.user)
			serializer = UserProfileReadSerializer(members, many=True)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)
		

	def perform_create(self,serializer):
		up = UserProfile.objects.get(user=self.request.user)
		group = serializer.save()
		status = GroupStatus(group=group,user=up,status=GroupStatus.ADMIN)
		status.save()


def is_user_in_group(user,group):
	try:
		group_status = GroupStatus.objects.get(group=group,user=user)
		if group_status.status!=GroupStatus.PENDING:
			return True
		return False
	except ObjectDoesNotExist :
		return False	

def is_user_admin_in_group(user,group):
	try:
		group_status = GroupStatus.objects.get(group=group,user=user)
		if group_status.status==GroupStatus.ADMIN:
			return True
		return False
	except ObjectDoesNotExist :
		return False