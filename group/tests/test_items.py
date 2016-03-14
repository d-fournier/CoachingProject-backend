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

    def test_create_group_anonymous(self):
        """
        Ensure we can't create a post as an anonymous user
        """
        url = reverse('groups-list')
        response = self.client.post(url, self.privateFalse)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_group_connected(self):
        """
        Ensure we can create a post if connected
        """
        url = reverse('groups-list')
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(url, self.privateFalse)
        self.client.force_authenticate(user=None)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_empty_list_anonymous(self):
        """
        Ensure no item
        """
        url = reverse('groups-list')
        response = self.client.get(url)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(responseData), 0)

    def test_get_list_anonymous(self):
        """
        Ensure item is present after insertion
        """
        # Insert init data
        Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        # Check get List
        url = reverse('groups-list')
        response = self.client.get(url)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(responseData), 1)

    def test_get_item_not_private_anonymous(self):
        """
        Ensure we can access to the item if it is not private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        # Check get List
        url = reverse('groups-detail', kwargs={'pk': group.id})
        response = self.client.get(url)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(responseData['id'], group.id)

    def test_get_item_private_anonymous(self):
        """
        Ensure we cannot access to the item if it is private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        # Check get List
        url = reverse('groups-detail', kwargs={'pk': group.id})
        response = self.client.get(url)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item_private_connected(self):
        """
        Ensure we cannot access to the item if it is private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        # Check get List
        url = reverse('groups-detail', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_item_not_private_connected(self):
        """
        Ensure we can access to the item if it is not private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        # Check get List
        url = reverse('groups-detail', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item_not_private_connected_member(self):
        """
        Ensure we can access to the item if it is not private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=False)
        GroupStatus.objects.create(user=self.user1Profile,group=group,status=GroupStatus.MEMBER)
        # Check get List
        url = reverse('groups-detail', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_item_private_connected_member(self):
        """
        Ensure we can access to the item if it is private
        """
        # Insert init data
        group = Group.objects.create(sport=self.sport, name="NAME" ,description="DESCRIPTION" ,city="CITY", private=True)
        GroupStatus.objects.create(user=self.user1Profile,group=group,status=GroupStatus.MEMBER)
        # Check get List
        url = reverse('groups-detail', kwargs={'pk': group.id})
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(url)
        self.client.force_authenticate(user=None)
        responseData = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)










    # def test_update_item_connected(self):
    #     """
    #     Ensure the creator can update the item
    #     """
    #     # Insert init data
    #     post = Post.objects.create(sport=self.sport, title="TEST", description="TEST", content='TEST', author=self.user1Profile)
    #     # Check get List
    #     url = reverse('blog-detail', kwargs={'pk': post.id})
    #     data = {'title': "MODIF"}
    #     self.client.force_authenticate(user=self.user1)
    #     response = self.client.patch(url, data)
    #     self.client.force_authenticate(user=None)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_item_connected_other_user(self):
    #     """
    #     Ensure another user can't update the item
    #     """
    #     # Insert init data
    #     post = Post.objects.create(sport=self.sport, title="TEST", description="TEST", content='TEST', author=self.user1Profile)
    #     # Check get List
    #     url = reverse('blog-detail', kwargs={'pk': post.id})
    #     data = {'title': "MODIF"}
    #     self.client.force_authenticate(user=self.user2)
    #     response = self.client.patch(url, data)
    #     self.client.force_authenticate(user=None)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_delete_item_connected_user(self):
    #     """
    #     Ensure another user can't update the item
    #     """
    #     # Insert init data
    #     post = Post.objects.create(sport=self.sport, title="TEST", description="TEST", content='TEST', author=self.user1Profile)
    #     # Check get List
    #     url = reverse('blog-detail', kwargs={'pk': post.id})
    #     self.client.force_authenticate(user=self.user2)
    #     response = self.client.delete(url)
    #     self.client.force_authenticate(user=None)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
