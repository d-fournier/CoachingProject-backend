from rest_framework.permissions import BasePermission, SAFE_METHODS

class PostAccessPermission(BasePermission):
	def has_permission(self,request, view):
		if request.method in SAFE_METHODS :
			return True
		elif request.user.is_authenticated() and request.method != 'DELETE':
			return True
		elif request.user.is_superuser:
			return True
		return False

	def has_object_permission(self, request, view, obj):
		return (obj.author.user == request.user) | request.user.is_superuser
