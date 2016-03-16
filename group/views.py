from django.db.models import Q, F
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from device import scripts
from message.models import Message
from message.serializers import MessageReadSerializer
from user.models import UserProfile
from user.serializers import UserProfileReadSerializer
from .functions import *
from .permissions import GroupPermission
from .serializers import GroupReadSerializer, GroupCreateSerializer


# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [GroupPermission]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return GroupReadSerializer
        return GroupCreateSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Group.objects.all()
        queryset = Group.objects.none()
        if self.action == 'list':
            if self.request.user.is_authenticated():
                queryset = Group.objects.all()
                up = UserProfile.objects.get(user=self.request.user)
                groupStatus = GroupStatus.objects.exclude(Q(user=up, status=GroupStatus.MEMBER) | Q(user=up,
                                                                                                    status=GroupStatus.ADMIN))  # Groupe où on est pas
                for gs in groupStatus:  # Je retire les grousp où on est pas
                    if gs.group.private:  # et qui sont privés
                        queryset = queryset.exclude(id=gs.group.id)
            else:
                queryset = Group.objects.filter(private=False)
        else:
            queryset = Group.objects.filter()
        keywords = self.request.query_params.get('keywords', None)
        if keywords is not None:
            queryset = queryset.filter(name__icontains=keywords) | queryset.filter(description__icontains=keywords)
        sport = self.request.query_params.get('sport', None)
        if sport is not None:
            queryset = queryset.filter(sport__id=sport)
        city = self.request.query_params.get('city', None)
        if city is not None:
            queryset = queryset.filter(city=city)
        return queryset

    @list_route()
    def my_groups(self, request):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            groupStatus = GroupStatus.objects.filter(
                Q(user=up, status=GroupStatus.MEMBER) | Q(user=up, status=GroupStatus.ADMIN))
            groups = []
            for gs in groupStatus:
                groups.append(Group.objects.get(pk=gs.group.id))
            serializer = GroupReadSerializer(groups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['get'])
    def messages(self, request, pk=None):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            group = get_group(pk)
            if group is None:
                return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            if is_user_in_group(up, group):
                queryset = Message.objects.filter(to_group=group).order_by('time')
            else:
                return Response('You are not a member of the group', status=status.HTTP_403_FORBIDDEN)

        else:
            return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)
        serializer = MessageReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def is_admin(self, request, pk=None):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            group = get_group(pk)
            return Response(is_user_admin_in_group(up, group), status=status.HTTP_200_OK)
        else:
            return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['get'])
    def user_status(self, request, pk=None):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            group = get_group(pk)
            if is_user_pending(up, group) or is_user_in_group(up, group):
                response = GroupStatus.objects.get(user=up,group=group).status
            else:
                response = 'NOT IN GROUP'
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @list_route()
    def my_invitations(self, request):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            queryset = GroupStatus.objects.filter(user=up, status=GroupStatus.INVITED)
            groups = []
            for q in queryset:
                groups.append(q.group)
            serializer = GroupReadSerializer(groups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def accept_invite(self, request, pk=None):
        if request.user.is_authenticated():
            group = get_group(pk)
            if group is None:
                return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            up = UserProfile.objects.get(user=request.user)
            try:
                invited_user_group_status = GroupStatus.objects.get(group=group, user=up, status=GroupStatus.INVITED)
            except ObjectDoesNotExist:
                return Response('You have not been invited in this group', status=status.HTTP_400_BAD_REQUEST)
            if request.data['accepted']:
                invited_user_group_status.status = GroupStatus.MEMBER
                invited_user_group_status.save()
                group.members = F('members') + 1
                group.save()
                return Response('Invitation successfully accepted', status=status.HTTP_200_OK)
            else:
                invited_user_group_status.delete()
                return Response('Invitation successfully refused', status=status.HTTP_200_OK)
        return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def accept_join(self, request, pk=None):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            group = get_group(pk)
            if group is None:
                return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            if is_user_admin_in_group(up, group):
                pending_users_id = request.data['users']
                for pk_user in pending_users_id:
                    try:
                        pending_user = UserProfile.objects.get(pk=pk_user)
                        pending_user_group_status = GroupStatus.objects.get(group=group, user=pending_user)
                    except ObjectDoesNotExist:
                        return Response('User is not registered or not in the group',
                                        status=status.HTTP_400_BAD_REQUEST)
                    if request.data['accepted']:  # Demande d'ajout acceptée
                        if pending_user_group_status.status == GroupStatus.PENDING:
                            pending_user_group_status.status = GroupStatus.MEMBER
                            pending_user_group_status.save()
                            group.members = F('members') + len(pending_users_id)
                            group.save()
                            scripts.sendGCMGroupJoinAccepted([pending_user], group)
                            return Response(pending_user.displayName + ' added to the group with success',
                                            status=status.HTTP_200_OK)
                        else:
                            return Response(pending_user.displayName + ' is already in the group',
                                            status=status.HTTP_400_BAD_REQUEST)
                    else:  # Demande d'ajout refusée
                        pending_user_group_status.delete()
                        return Response('Demand from ' + pending_user.displayName + ' refused',
                                        status=status.HTTP_200_OK)
            else:
                return Response('You are not admin of this group', status=status.HTTP_403_FORBIDDEN)
        return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def join(self, request, pk=None):
        if request.user.is_authenticated():
            group = get_group(pk)
            if group is None:
                return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            if group.private:
                return Response('This group is private', status=status.HTTP_403_FORBIDDEN)
            up = UserProfile.objects.get(user=request.user)
            try:
                status_pending = GroupStatus.objects.get(group=group, user=up)
                return Response('You are already in the group or asked to join it', status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                status_pending = GroupStatus(group=group, user=up, status=GroupStatus.PENDING)
                status_pending.save()
                admins = GroupStatus.objects.filter(group=group, status=GroupStatus.ADMIN)
                users = []
                for a in admins:
                    users.append(a.user)
                scripts.sendGCMGroupJoin(users, group)
                return Response('Demand created and sent to the group', status=status.HTTP_201_CREATED)
        return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def invite(self, request, pk=None):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            group = get_group(pk)
            if group is None:
                return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            if is_user_admin_in_group(up, group):
                invited_users_id = request.data['users']
                for pk_user in invited_users_id:
                    try:
                        invited_user = UserProfile.objects.get(pk=pk_user)
                    except ObjectDoesNotExist:
                        return Response('User given is not registered', status=status.HTTP_400_BAD_REQUEST)
                    try:
                        invited_user_group_status = GroupStatus.objects.get(group=group, user=invited_user)
                        return Response(invited_user.displayName + ' is already in the group or asked to join it',
                                        status=status.HTTP_400_BAD_REQUEST)
                    except ObjectDoesNotExist:
                        invited_user_group_status = GroupStatus(group=group, user=invited_user,
                                                                status=GroupStatus.INVITED)
                        invited_user_group_status.save()
                        scripts.sendGCMGroupInvite([invited_user], group)
                        return Response(invited_user.displayName + ' invited to the group with success',
                                        status=status.HTTP_200_OK)
            else:
                return Response('You are not admin of this group', status=status.HTTP_403_FORBIDDEN)
        return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def leave(self, request, pk=None):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            group = get_group(pk)
            if group is None:
                return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            if not is_user_admin_in_group(up,group):
                try:
                    leave_user_status = GroupStatus.objects.get(group=group, user=up)
                    leave_user_status.delete()
                    group.members = F('members') - 1
                    if group.members == 0:
                        group.delete()
                    group.save()
                    return Response('You left the group with success',status=status.HTTP_200_OK)
                except ObjectDoesNotExist:
                    return Response('You are not in the group',status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('You are admin of the group, you cannot leave it', status=status.HTTP_403_FORBIDDEN)
        else:
            return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['get'])
    def pending_members(self, request, pk=None):
        if request.user.is_authenticated():
            group = get_group(pk)
            if group is None:
                return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            up = UserProfile.objects.get(user=request.user)
            if is_user_admin_in_group(up, group):
                status_members = GroupStatus.objects.filter(group=group, status=GroupStatus.PENDING)
                members = []
                for s in status_members:
                    members.append(s.user)
                serializer = UserProfileReadSerializer(members, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('You are not admin of this group', status=status.HTTP_403_FORBIDDEN)
        else:
            return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['get'])
    def members(self, request, pk=None):
        if request.user.is_authenticated():
            up = UserProfile.objects.get(user=request.user)
            group = get_group(pk)
            if group is None:
                return Response('Group not found', status=status.HTTP_404_NOT_FOUND)
            if group.private and not is_user_in_group(up, group):
                return Response('This group is private', status=status.HTTP_403_FORBIDDEN)
            status_members = GroupStatus.objects.filter(
                Q(group=group, status=GroupStatus.MEMBER) | Q(group=group, status=GroupStatus.ADMIN))
            members = []
            for s in status_members:
                members.append(s.user)
            serializer = UserProfileReadSerializer(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('You are not connected', status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        up = UserProfile.objects.get(user=self.request.user)
        group = serializer.save()
        new_status = GroupStatus(group=group, user=up, status=GroupStatus.ADMIN)
        new_status.save()
