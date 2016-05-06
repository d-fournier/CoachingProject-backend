from rest_framework import viewsets

from user.models import UserProfile
from .models import Post
from .permissions import PostAccessPermission
from .serializers import PostReadSerializer, PostCreateUpdateSerializer


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	permission_classes= [PostAccessPermission,]

	def get_serializer_class(self):
		if self.action=='list' or self.action=='retrieve':
			return PostReadSerializer
		else:
			return PostCreateUpdateSerializer

	def perform_create(self,serializer):
		up = UserProfile.objects.get(user=self.request.user)
		serializer.save(author=up)
