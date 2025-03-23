from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from users.serializers import (
    EmptySerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.generics import (
    RetrieveAPIView,
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet, ModelViewSet, ReadOnlyModelViewSet

User = get_user_model()


class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        serializer_class=UserRegistrationSerializer,
    )
    def register(self, request):
        """Register a new user"""

        if request.user.is_authenticated:
            return JsonResponse(
                {"error": "Authenticated users cannot register new users."},
                status=403,
            )

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        serializer_class=EmptySerializer,
    )
    def logout(self, request):
        """Logout the current user by blacklisting their refresh token."""

        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST
            )


class RetrieveUpdateCurrentUserView(RetrieveAPIView, UpdateAPIView):
    # Using APIViews instead of mixins because of automatic method binding
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
