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
from auth_djoser import views
from django.contrib.auth import get_user_model


from sport.views import SportViewSet
from level.views import LevelViewSet
from user.views import UserProfileViewSet
from relation.views import RelationViewSet

router = routers.DefaultRouter()
router.register(r'sports', SportViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'users', UserProfileViewSet, base_name='users')
router.register(r'relations', RelationViewSet)

User = get_user_model()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
   	url(r'^api-auth/', include('rest_framework.urls')),
   	url(r'^api/', include(router.urls)),
    url(r'^me/$', views.UserView.as_view(), name='user'),
    url(r'^register/$', views.RegistrationView.as_view(), name='register'),
    url(r'^activate/$', views.ActivationView.as_view(), name='activate'),
    url(r'^{0}/$'.format(User.USERNAME_FIELD), views.SetUsernameView.as_view(), name='set_username'),
    url(r'^password/$', views.SetPasswordView.as_view(), name='set_password'),
    url(r'^password/reset/$', views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm/$', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^$', views.RootView.as_view(urls_extra_mapping={'login': 'login', 'logout': 'logout'}), name='root'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]

