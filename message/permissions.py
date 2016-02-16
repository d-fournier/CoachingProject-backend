from rest_framework import permissions
from .models import Message
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
				if request.method=='POST':
					return True
				else:
					return False
			else:
				return False