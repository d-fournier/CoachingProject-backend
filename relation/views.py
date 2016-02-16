from django.shortcuts import render
from .serializers import RelationReadSerializer, RelationCreateSerializer
from .models import Relation
from .permissions import RelationAccessPermission
from rest_framework import viewsets, permissions
from user.models import UserProfile
from message.models import Message
from django.db.models import Q
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from message.serializers import MessageReadSerializer



# Create your views here.
class RelationViewSet(viewsets.ModelViewSet):
	queryset = Relation.objects.all()
	permission_classes= [RelationAccessPermission,]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return RelationReadSerializer
		return RelationCreateSerializer
 
	def get_queryset(self):		
		if self.request.user.is_authenticated():
			queryset = Relation.objects.filter(Q(coach__user=self.request.user)|Q(trainee__user=self.request.user))
		else:
			queryset=Relation.objects.none()
		return queryset

	@detail_route(methods=['get'])
	def messages(self,request, pk=None):
		queryset=Message.objects.none()
		relation=Relation.objects.get(pk=pk)
		if request.user.is_authenticated():
			profile=UserProfile.objects.get(user=request.user)
			if (relation.coach == profile) | (relation.trainee == profile):
				queryset=Message.objects.filter(to_relation=relation).order_by('time')
		serializer=MessageReadSerializer(queryset, many=True)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_200_OK,headers=headers)

	def create(self,request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			data = serializer.validated_data
			if ((data.get('trainee').user==self.request.user) | (data.get('coach').user==self.request.user)):
				self.object = serializer.save()
				self.object.save()
				headers = self.get_success_headers(serializer.data)
				return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

			return Response('Cannot create a relation you are not involved in', status=status.HTTP_401_UNAUTHORIZED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)