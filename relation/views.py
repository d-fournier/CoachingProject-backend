from django.shortcuts import render
from .serializers import RelationSerializer
from .models import Relation
from rest_framework import viewsets, permissions
from user.models import UserProfile
from message.models import Message
from django.db.models import Q
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from message.serializers import MessageSerializer


# Create your views here.
class RelationViewSet(viewsets.ModelViewSet):
	queryset = Relation.objects.all()
	serializer_class = RelationSerializer
	permission_classes= [permissions.IsAuthenticatedOrReadOnly]

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
		serializer=MessageSerializer(queryset, many=True)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_200_OK,headers=headers)
