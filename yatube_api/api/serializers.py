from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow

from djoser.serializers import UserSerializer

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ("username", "password")


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = "__all__"
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    post = serializers.SlugRelatedField(read_only=True, slug_field="pk")

    class Meta:
        fields = "__all__"
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        read_only=False, slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                Follow.objects.all(),
                fields=["user", "following"])
        ]

    def validate(self, data):
        if self.context["request"].user == data["following"]:
            raise serializers.ValidationError(
                "Подписка на самого себя запрещена"
            )
        return data
