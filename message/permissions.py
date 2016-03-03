from rest_framework import permissions
from .models import Message
from user.models import UserProfile
from .serializers import MessageReadSerializer

class MessagePermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
		# Check permissions for read-only request
			return True
		else:
			# Check permissions for write request
			if request.user.is_superuser:
				return True
			elif request.user.is_authenticated():
				if request.method=='POST' and request.method=='PATCH':
					return True
				else:
					return False
			else:
				return False

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			if request.user.is_superuser:
				return True
			if request.user.is_authenticated():
				up = UserProfile.objects.get(user=request.user)
				relation, group = obj.to_relation, obj.to_group
				if relation is not None :
					if relation.coach==up or relation.trainee==up :
						return True
				if group is not None :
					if up in group.members.all() :
						return True
				return False
			else:
				return False
