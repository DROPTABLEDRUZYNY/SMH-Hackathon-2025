from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views import GetCSRFToken, LeaderboardView

from . import views

router = DefaultRouter()
#router.register(r"products1", views.ProductViewSet, basename="products1")
#router.register(r"products2", views.ProductItemsViewSet, basename="products2")

router.register(r"trash_places", views.TrashPlaceListViewSet, basename="trash_places")
router.register(r"activities", views.ActivityViewSet, basename="activities")

urlpatterns = [
    path("", include(router.urls)),
    path("random/", views.RandomProductView.as_view(), name="random_product"),
    
    path("csrf/", GetCSRFToken.as_view(), name="get_csrf"),
    
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path("api-auth/", include("rest_framework.urls")),  # auth ONLY for browsable API 
    path("users/", include("users.urls")),
]
