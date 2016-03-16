from django.db import IntegrityError
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from device import scripts
from message.models import Message
from message.serializers import MessageReadSerializer
from user.models import UserProfile
from .models import Relation
from .permissions import RelationAccessPermission
from .serializers import RelationReadSerializer, RelationCreateSerializer, RelationUpdateSerializer


# Create your views here.
class RelationViewSet(viewsets.ModelViewSet):
	queryset = Relation.objects.all()
	permission_classes= [RelationAccessPermission,]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return RelationReadSerializer
		elif self.action=='partial_update':
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
		try:
			relation=Relation.objects.get(pk=pk)
		except:
			return Response('Relation not found', status=status.HTTP_404_NOT_FOUND)
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
			scripts.sendGCMCoachingCreation(users=[coach],relation=r)#We use the coach because it's the trainee who ask for coaching
		except IntegrityError:
			raise ValidationError('One relation has already been created between this coach and this trainee for the given sport')

	def perform_update(self,serializer):
		relation = serializer.instance
		previous_requestStatus = relation.requestStatus
		previous_active = relation.active
		data = serializer.validated_data
		up = UserProfile.objects.get(user=self.request.user)
		authorized_set = set(['requestStatus','active'])
		key_set = set([x for x in data.keys()])
		if relation.requestStatus!=None and 'requestStatus' in key_set:
			raise ValidationError('You cannot update the requestStatus of this relation because it has already been set')
		if not key_set.issubset(authorized_set) :
			raise ValidationError('You can only update status and active attributes of a Relation')
		r = serializer.save()
		if previous_requestStatus==None and r.requestStatus!=None:
			scripts.sendGCMCoachingResponse(users=([r.trainee] if r.coach==up else [r.coach]),relation=r)
		elif previous_active==True and r.active==False :
			scripts.sendGCMCoachingEnd(users=([r.trainee] if r.coach==up else [r.coach]),relation=r)
