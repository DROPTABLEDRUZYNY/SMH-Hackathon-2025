from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from users.serializers import UserSerializer

# Create your views here.
User = get_user_model()


class UserViewSet(ReadOnlyModelViewSet):
    """Dev endpoint"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveCurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
