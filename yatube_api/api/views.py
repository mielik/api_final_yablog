from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from http import HTTPStatus
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from django.http import HttpResponse
from rest_framework import permissions, viewsets, exceptions
from rest_framework.pagination import LimitOffsetPagination
from posts.models import Post, Group, Follow
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
)
from .permissions import IsAuthorOrReadOnlyPermission


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated:
            raise exceptions.NotAuthenticated(
                "Неавторизованный пользователь не может создавать пост"
            )
        serializer.save(author=user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super().perform_update(serializer)

    def perform_destroy(self, _):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        author = self.request.user
        if not author.is_authenticated:
            raise exceptions.NotAuthenticated(
                "Неавторизованный пользователь не может создавать пост"
            )
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(Post, id=(self.kwargs.get("post_id"))),
        )

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого контента запрещено!")
        super().perform_update(serializer)

    def perform_destroy(self, _):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("Удаление чужого контента запрещено!")
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save(
                self.request.user,
                group=Group.objects.create(),
            )
        return HttpResponse(status_osde=HTTPStatus.METHOD_NOT_ALLOWED)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("user__username", "following__username")

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
