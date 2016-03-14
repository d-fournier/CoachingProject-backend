from django.shortcuts import render
from .serializers import UserProfileReadSerializer, UserProfileCreateSerializer
from .models import UserProfile
from .permissions import UserProfilePermission
from blog.models import Post
from blog.serializers import PostReadSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route

# Create your views here.
class UserProfileViewSet(viewsets.ModelViewSet):
	permission_classes= [UserProfilePermission]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return UserProfileReadSerializer
		return UserProfileCreateSerializer

	def get_queryset(self):
		queryset = UserProfile.objects.all()
		keywords = self.request.query_params.get('keywords', None)
		if keywords is not None :
			queryset = queryset.filter(displayName__icontains=keywords)|queryset.filter(description__icontains=keywords)
		coach = self.request.query_params.get('coach', None)
		if coach is not None :
			queryset = queryset.filter(isCoach=coach)
		sport = self.request.query_params.get('sport', None)
		if sport is not None :
			queryset = queryset.filter(levels__sport__id=sport)
		level = self.request.query_params.get('level', None)
		if level is not None :
			queryset = queryset.filter(levels__id=level)
		return queryset

	@list_route()
	def me(self, request):
		if request.user.is_authenticated():
			queryset = UserProfile.objects.get(user=request.user)
			serializer = UserProfileReadSerializer(queryset)
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_200_OK,headers=headers)
		return Response('You are not connected', status=status.HTTP_403_FORBIDDEN)

	@detail_route(methods=['get'])
	def blog(self,request,pk=None):
		if request.user.is_authenticated() :
			up = UserProfile.objects.get(user=request.user)
			posts = Post.objects.filter(author=up).order_by('last_modification_date')
			serializer = PostReadSerializer(posts,many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)


	def perform_update(self, serializer):
		oldUp = UserProfile.objects.get(user=self.request.user)
		serializer.save()
		oldUp.picture.delete()

	def perform_destroy(self, instance):
		instance.picture.delete()
		instance.delete()

