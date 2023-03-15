from rest_framework import generics, permissions, status
from rest_framework.response import Response

from posts.models import Follow
from posts.serializers import FollowSerializer


class FollowListCreateView(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if "search" in request.query_params:
            query = request.query_params["search"]
            follows = Follow.objects.filter(
                user=request.user, following__username__icontains=query
            )
        else:
            follows = Follow.objects.filter(user=request.user)
        serializer = self.serializer_class(follows, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        following_user = request.data.get("following")
        if following_user == request.user.id:
            return Response(
                {"error": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(
            data={"user": request.user.id, "following": following_user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
