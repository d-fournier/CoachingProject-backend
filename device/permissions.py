from rest_framework.permissions import BasePermission, SAFE_METHODS
from user.models import UserProfile

class DevicePermission(BasePermission):
	def has_permission(self,request, view):
		if request.method in SAFE_METHODS :
			if request.user.is_superuser:
				return True
			return False
		if request.user.is_authenticated():
			if request.method=='POST' or request.method=='DELETE':
				return True
		return False

	def has_object_permission(self, request, view, obj):
		up = UserProfile.objects.get(user=request.user)
		return request.user.is_superuser or up==obj.user