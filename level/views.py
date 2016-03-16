from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from sport.serializers import SportSerializer
from .models import Level
from .serializers import LevelReadSerializer, LevelCreateSerializer


# Create your views here.
class LevelViewSet(viewsets.ModelViewSet):
	queryset = Level.objects.all()
	permission_classes= [permissions.DjangoModelPermissionsOrAnonReadOnly]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return LevelReadSerializer
		return LevelCreateSerializer

	@detail_route(methods=['get'])
	def sport(self, request, pk=None):
		level = Level.objects.get(pk=pk)
		queryset = level.sport
		serializer = SportSerializer(queryset)
		return Response(serializer.data, status=status.HTTP_200_OK)