from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
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

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.views import View
import json


@method_decorator(ensure_csrf_cookie, name="dispatch")
@extend_schema(
    summary="User Login",
    description="Authenticate a user using email and password. ",
    request={
        "type": "object",
        "properties": {
            "email": {"type": "string", "example": "admin@admin.pl"},
            "password": {"type": "string", "example": "admin"},
        },
    },
)
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body or "{}")
        username = data.get("email")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

        login(request, user)
        return JsonResponse({"message": "Logged in successfully"})


@extend_schema(
    summary="User Logout",
    description="Logs out the currently authenticated user. Returns a success message.",
    responses={200: {"type": "object", "properties": {"message": {"type": "string"}}}},
)
class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"message": "Logged out"})


@extend_schema_view(
    list=extend_schema(
        summary="List Users",
        description="Retrieve a list of all registered users.",
        responses={200: UserSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve User",
        description="Retrieve details of a specific user by ID.",
        responses={200: UserSerializer},
    ),
)
class UserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        summary="Register a New User",
        description="Allows a new user to register by providing required details.",
        request=UserRegistrationSerializer,
    )
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        serializer_class=UserRegistrationSerializer,
    )
    def register(self, request):
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


@extend_schema(
    summary="Retrieve or Update Current User",
    description="Retrieve or update the currently authenticated user's details.",
    responses={200: UserSerializer},
)
class RetrieveUpdateCurrentUserView(RetrieveAPIView, UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
