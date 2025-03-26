from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LoginView, LogoutView

from . import views

router = DefaultRouter()
router.register(r"", views.UserViewSet, basename="users")   # Including /register and more

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "current/",
        views.RetrieveUpdateCurrentUserView.as_view(),
        name="user_current",
    ),
    path("", include(router.urls)),
]
