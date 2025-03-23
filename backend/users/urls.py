from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"", views.UserViewSet, basename="users")

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path(
        "current/",
        views.RetrieveUpdateCurrentUserView.as_view(),
        name="user_current",
    ),
    path("", include(router.urls)),
]
