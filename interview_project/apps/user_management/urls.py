from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("retrieve-token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
]
