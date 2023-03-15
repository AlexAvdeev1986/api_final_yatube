from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import ListAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404

from posts.models import Post, Group
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer)
from .permissions import IsAuthorOrAuthenticatedReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """CRUD класс для модели Post"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrAuthenticatedReadOnly, )
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Получение инстанса автора для сохраннения в модели Post"""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """CRUD класс для модели Group"""
    permission_classes = (permissions.AllowAny,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(ListAPIView, CreateModelMixin, GenericViewSet):
    """CRUD класс для модели Follow"""
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        """Получение подписок для user из request"""
        return self.request.user.follower

    def perform_create(self, serializer):
        """Получчение инстанса автора для сохраннения в модели Follow"""
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """CRUD класс для модели Comments"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAuthenticatedReadOnly, )

    def get_queryset(self):
        """Получение коментов для конкретного поста"""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        queryset = post.comments
        return queryset

    def perform_create(self, serializer):
        """
        Получение инстанса поста и автора для сохранения в модели коментов
        """
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(
            author=self.request.user,
            post=post
        )
