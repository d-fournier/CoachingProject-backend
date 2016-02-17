from rest_framework.permissions import BasePermission, SAFE_METHODS

class RelationAccessPermission(BasePermission):
	def has_permission(self,request, view):
		if request.method in SAFE_METHODS :
			return True
		if request.user.is_authenticated():
			return True
		return False

	def has_object_permission(self, request, view, obj):
		# Instance must have an attribute named `coach` and 'trainee'.
		return (obj.trainee.user == request.user) | (obj.coach.user == request.user) | request.user.is_superuser