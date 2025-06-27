from rest_framework import viewsets
from yatube.models import Group, Comment, User
from .serializers import GroupSerializer, CommentSerializer, UserSerializer
from .permissions import OwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (OwnerOrReadOnly,)

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter) 
    search_fields = ('name',) 
    filterset_fields = ("name", "user__username",)
    ordering_fields = ('name',) 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)
    queryset = Comment.objects.all()
    # def get_queryset(self):
    #     return Comment.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]