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



    def test_join_by_anonymous_private(self):
        """
        Ensure we cannot join if we are anonymous
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        # Check get List
        url = reverse('groups-join', kwargs={'pk': group.id})
        response = self.client.post(url)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_join_by_connected_private(self):
        """
        Ensure we cannot join if we are connected and the group is private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        # Check get List
        self.client.force_authenticate(user=self.user1)
        url = reverse('groups-join', kwargs={'pk': group.id})
        response = self.client.post(url)
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_join_by_member_private(self):
        """
        Ensure we can access to the item if it is private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        GroupStatus.objects.create(user=self.user1Profile,group=group,status=GroupStatus.MEMBER)
        # Check get List
        self.client.force_authenticate(user=self.user1)
        url = reverse('groups-join', kwargs={'pk': group.id})
        response = self.client.post(url)
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_join_by_anonymous_not_private(self):
        """
        Ensure we cannot join if we are anonymous
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        # Check get List
        url = reverse('groups-join', kwargs={'pk': group.id})
        response = self.client.post(url)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_join_by_connected_not_private(self):
        """
        Ensure we cannot join if we are connected and the group is private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        # Check get List
        self.client.force_authenticate(user=self.user1)
        url = reverse('groups-join', kwargs={'pk': group.id})
        response = self.client.post(url)
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_join_by_member_not_private(self):
        """
        Ensure we can access to the item if it is private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        GroupStatus.objects.create(user=self.user1Profile,group=group,status=GroupStatus.MEMBER)
        # Check get List
        self.client.force_authenticate(user=self.user1)
        url = reverse('groups-join', kwargs={'pk': group.id})
        response = self.client.post(url)
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
