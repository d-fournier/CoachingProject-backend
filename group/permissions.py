from rest_framework import permissions
from user.models import UserProfile
from .functions import is_user_in_group

class GroupPermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
		# Check permissions for read-only request
			return True
		else:
			# Check permissions for write request
			if request.user.is_superuser:
				return True
			elif request.user.is_authenticated():
				if request.method=='POST':
					return True
				else:
					return False
			else:
				return False

	def has_object_permission(self, request, view, obj):
		if obj.private :
			if request.user.is_authenticated() :
				up = UserProfile.objects.get(user=request.user)
				if is_user_in_group(up,obj):
					return True
			return False
		else:
			if request.method in permissions.SAFE_METHODS:
				return True
			else:
				if request.user.is_superuser:
					return True
				else:
					return False
