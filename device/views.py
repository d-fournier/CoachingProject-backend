from rest_framework import viewsets, status
from .permissions import DevicePermission
from .models import Device
from user.models import UserProfile
from .serializers import DeviceReadSerializer,DeviceCreateSerializer
from django.db import IntegrityError

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
		try:
			serializer.save(user=up)
		except IntegrityError:
			device = Device.objects.get(user=up,device_id=serializer.validated_data.get('device_id'))
			device.registration_token = serializer.validated_data.get('registration_token')
			device.name = serializer.validated_data.get('name')
			device.save()

		
		
