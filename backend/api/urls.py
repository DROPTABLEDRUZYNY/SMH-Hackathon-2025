from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from . import views

router = DefaultRouter()
router.register(r"products1", views.ProductItemsView, basename="products1")
router.register(r"products2", views.ProductViewSet, basename="products2")
router.register(r"products3", views.ProductReadOnlyViewSet, basename="products3")

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    path("random/", views.get_random_product), 
    # path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    # path('v2/products/<int:pk>/', views.ProductDetailView2.as_view({'get': 'retrieve'}), name='product-detail'),
]
