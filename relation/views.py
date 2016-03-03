from django.shortcuts import render
from .serializers import RelationReadSerializer, RelationCreateSerializer
from .models import Relation
from .permissions import RelationAccessPermission
from rest_framework import viewsets, permissions, status
from user.models import UserProfile
from message.models import Message
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import detail_route
from rest_framework.response import Response
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
		if self.request.user.is_superuser :
			queryset = Relation.objects.all()
		elif self.request.user.is_authenticated():
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


	def perform_create(self,serializer):
		data = serializer.validated_data
		trainee = UserProfile.objects.get(user=self.request.user)
		coach = data.get('coach')
		if not coach.isCoach:
			raise ValidationError('The person you asked for coaching is not a coach')
		if coach.user==trainee.user:
			raise ValidationError('Coach and trainee must be different')
		serializer.save(trainee=trainee)

	def perform_update(self,serializer):
		data = serializer.validated_data
		if [x for x in data.keys()] != ['requestStatus','active']:
			raise ValidationError('You can only update status and active attributes of a Relation')
		serializer.save()
