"""SIMS_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings


from sport.views import SportViewSet
from level.views import LevelViewSet
from user.views import UserProfileViewSet
from relation.views import RelationViewSet
from message.views import MessageViewSet
from group.views import GroupViewSet

router = routers.DefaultRouter()
router.register(r'sports', SportViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'users', UserProfileViewSet, base_name='users')
router.register(r'relations', RelationViewSet)
router.register(r'messages', MessageViewSet, base_name='messages')
router.register(r'groups',GroupViewSet,base_name='groups')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
   	url(r'^api-auth/', include('rest_framework.urls')),
   	url(r'^api/', include(router.urls)),
    url(r'^auth/', include('auth_djoser.urls')),
]
if not settings.AWS_ACTIVATED:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.GCM_ACTIVATED:
    urlpatterns = urlpatterns + [url(r'', include('gcm.urls'))]

