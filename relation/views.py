from django.shortcuts import render
from .serializers import RelationReadSerializer, RelationCreateSerializer, RelationUpdateSerializer
from .models import Relation
from .permissions import RelationAccessPermission
from device import scripts
from rest_framework import viewsets, permissions, status
from user.models import UserProfile
from message.models import Message
from django.db.models import Q
from django.db import IntegrityError
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
		elif self.action=='update':
			return RelationUpdateSerializer
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
		try:
			r = serializer.save(trainee=trainee)
			scripts.sendGCMCoachingCreation(users=[trainee],relation=r)
		except IntegrityError:
			raise ValidationError('One relation has already been created between this coach and this trainee for the given sport')

	def perform_update(self,serializer):
		data = serializer.validated_data
		up = UserProfile.objects.get(user=self.request.user)
		authorized_set = set(['requestStatus','active'])
		key_set = set([x for x in data.keys()])
		if not key_set.issubset(authorized_set) :
			raise ValidationError('You can only update status and active attributes of a Relation')
		r = serializer.save()
		if r.relation.active:
			scripts.sendGCMCoachingResponse(users=([r.trainee] if r.coach==up else [r.coach]),relation=r)
		else:
			scripts.sendGCMCoachingEnd(users=([r.trainee] if r.coach==up else [r.coach]),relation=r)
