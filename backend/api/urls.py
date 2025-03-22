from django.urls import path, include
from rest_framework.routers import DefaultRouter


from . import views

router = DefaultRouter()
router.register(r"products1", views.ProductItemsViewSet, basename="products1")
router.register(r"products2", views.ProductViewSet, basename="products2")
router.register(r"products3", views.ProductReadOnlyViewSet, basename="products3")

urlpatterns = [
    path("", include(router.urls)),
    path("random/", views.get_random_product, name="random_product"),
    path("users/", include("users.urls")),
]
