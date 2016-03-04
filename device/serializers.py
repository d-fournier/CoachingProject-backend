from rest_framework import serializers
from .models import Device
from user.serializers import UserProfileReadSerializer

class DeviceReadSerializer(serializers.ModelSerializer):
	user = UserProfileReadSerializer(read_only=True)
	
	class Meta:
		model = Device
		fields = ('__all__')

class DeviceCreateSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Device
		fields = ('name','device_id','registration_token')