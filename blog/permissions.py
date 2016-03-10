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
		if request.method in SAFE_METHODS:
			return True
		else:
			if request.user.is_superuser:
				return True
			elif request.user.is_authenticated() and request.user == obj.author.user:
				return True
			else:
				return False
