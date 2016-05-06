from rest_framework import serializers
from .models import Device
from user.serializers import UserProfileReadSerializer

class DeviceReadSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Device
		fields = ('id','name','device_id','registration_token')

class DeviceCreateSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Device
		fields = ('name','device_id','registration_token')