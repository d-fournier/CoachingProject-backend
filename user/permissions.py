from rest_framework import permissions

class UserProfilePermission(permissions.BasePermission):
	
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
		# Check permissions for read-only request
			return True
		else:
		# Check permissions for write request
			if request.user.is_superuser:
				return True
			elif request.user.is_authenticated():
				if request.method=='PUT':
					return True
				else:
					return False
			else:
				return False


	def has_object_permission(self, request, view, obj):
		if request.user.id == obj.user.id or request.user.is_superuser:
			return True
		else:
			return False
