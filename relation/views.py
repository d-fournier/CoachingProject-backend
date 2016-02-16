from django.shortcuts import render
from .serializers import RelationSerializer
from .models import Relation
from rest_framework import viewsets, permissions

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
