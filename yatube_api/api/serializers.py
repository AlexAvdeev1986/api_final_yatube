from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Group, Follow


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        source="user",
    )
    following = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all(), source="following"
    )

    def validate_following(self, following):
        if following == self.context["request"].user:
            raise serializers.ValidationError("You cannot follow yourself.")
        return following

    class Meta:
        model = Follow
        fields = "__all__"
