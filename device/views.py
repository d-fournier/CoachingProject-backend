from rest_framework import viewsets, status
from .permissions import DevicePermission
from .models import Device
from user.models import UserProfile
from .serializers import DeviceReadSerializer,DeviceCreateSerializer

# Create your views here.
class DeviceViewSet(viewsets.ModelViewSet):
	queryset = Device.objects.all()
	permission_classes= [DevicePermission]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return DeviceReadSerializer
		return DeviceCreateSerializer

	def perform_create(self,serializer):
		up = UserProfile.objects.get(user=self.request.user)
		serializer.save(user=up)
