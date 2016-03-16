from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from device import scripts
from group.functions import is_user_in_group, get_members
from group.models import GroupStatus, Group
from user.models import UserProfile
from .models import Message
from .permissions import MessagePermission
from .serializers import MessageReadSerializer, MessageCreateSerializer, MessageUpdateSerializer


# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
	permission_classes= [MessagePermission]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return MessageReadSerializer
		elif self.action=='partial_update':
			return MessageUpdateSerializer
		return MessageCreateSerializer

	def get_queryset(self):	
		if self.request.user.is_superuser:
			queryset = Message.objects.all()	
		elif self.request.user.is_authenticated():
			up = UserProfile.objects.get(user=self.request.user)
			groupStatus = GroupStatus.objects.filter(Q(user=up,status=GroupStatus.MEMBER)|Q(user=up,status=GroupStatus.ADMIN))
			groups = []
			for gs in groupStatus :
				groups.append(Group.objects.get(pk=gs.group.id))
			queryset = Message.objects.filter(Q(to_relation__coach__user=self.request.user)|Q(to_relation__trainee__user=self.request.user)|Q(to_group__in=groups))
		else:
			queryset=Message.objects.none()
		return queryset

	def perform_create(self,serializer):
		data = serializer.validated_data
		up = UserProfile.objects.get(user=self.request.user)
		users = []
		relation, group = serializer.validated_data.get('to_relation'), serializer.validated_data.get('to_group')
		if relation is not None and group is not None :
			raise ValidationError('You cannot have a relation and a group for the same message, one should be null')
		if relation is not None :
			if relation.requestStatus!=True :
				raise ValidationError('You cannot send a message because the relation is not confirmed')
			if relation.coach!=up and relation.trainee!=up:
				raise ValidationError('You cannot send a message because you are not involved in this relation')
			users.append(relation.trainee if relation.coach==up else relation.coach)
		if group is not None :
			if not is_user_in_group(up,group):
				raise ValidationError('You cannot send a message because you are not a member of this group')
			users = get_members(group)
			users.remove(up)		
		m = serializer.save(from_user=up)
		scripts.sendGCMNewMessage(users=users,message=m)
		

	def perform_partial_update(self,serializer):
		try :
			associated_file = serializer.validated_data['associated_file']
		except KeyError:
			raise ValidationError('Field missing : associated_file')
		message = serializer.instance
		message.associated_file = associated_file