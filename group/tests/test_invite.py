from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import AnonymousUser, User
from user.models import UserProfile
from sport.models import Sport
from group.models import Group,GroupStatus
from datetime import datetime
import json

class GroupTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='testuser1', email='username@example.com', password='password')
        self.user2 = User.objects.create(username='testuser2', email='username@example.com', password='password')
        self.sport = Sport.objects.create(name='test_sport')
        self.user1Profile = UserProfile.objects.create(user=self.user1, displayName = 'TestUser1', birthdate = datetime.now(), isCoach = False, city = 'Lyon', description = '')
        self.user2Profile = UserProfile.objects.create(user=self.user2, displayName = 'TestUser2', birthdate = datetime.now(), isCoach = False, city = 'Lyon', description = '')

        self.privateFalse = {'sport': self.sport.id ,'name':"NAME" ,'description':"DESCRIPTION" ,'city':"CITY", 'private':False }
        self.privateTrue = {'sport': self.sport.id ,'name':"NAME" ,'description':"DESCRIPTION" ,'city':"CITY", 'private':True }
    
    def test_invite_by_member_private(self):
        """
        Ensure we cannot invite if we are not admin
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        GroupStatus.objects.create(user=self.user1Profile,group=group,status=GroupStatus.MEMBER)
        # Check get List
        url = reverse('groups-invite', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url,{'users':[self.user2.id]})
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_by_anonymous_private(self):
        """
        Ensure we cannot invite if we are not admin
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        # Check get List
        url = reverse('groups-invite', kwargs={'pk': group.id})
        response = self.client.post(url,{'users':[self.user2.id]})
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invite_by_connected_private(self):
        """
        Ensure we cannot invite if we are not admin
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        # Check get List
        url = reverse('groups-invite', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url,{'users':[self.user2.id]})
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_by_admin_private(self):
        """
        Ensure we can invite if we are admin
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        GroupStatus.objects.create(user=self.user1Profile,group=group,status=GroupStatus.ADMIN)
        # Check get List
        url = reverse('groups-invite', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url,{'users':[self.user2.id]})
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invite_by_member_not_private(self):
        """
        Ensure we cannot invite if we are not admin
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        GroupStatus.objects.create(user=self.user1Profile,group=group,status=GroupStatus.MEMBER)
        # Check get List
        url = reverse('groups-invite', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url,{'users':[self.user2.id]})
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_by_anonymous_not_private(self):
        """
        Ensure we cannot invite if we are not admin
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        # Check get List
        url = reverse('groups-invite', kwargs={'pk': group.id})
        response = self.client.post(url,{'users':[self.user2.id]})
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invite_by_admin_not_private(self):
        """
        Ensure we can invite if we are admin
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        GroupStatus.objects.create(user=self.user1Profile,group=group,status=GroupStatus.ADMIN)
        # Check get List
        url = reverse('groups-invite', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url,{'users':[self.user2.id]})
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invite_by_connected_not_private(self):
        """
        Ensure we cannot invite if we are not admin
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        # Check get List
        url = reverse('groups-invite', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url,{'users':[self.user2.id]})
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)