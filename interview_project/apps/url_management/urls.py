from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RedirectRuleViewSet

router = DefaultRouter()
router.register(r"url", RedirectRuleViewSet, basename="url")

urlpatterns = [
    path("", include(router.urls)),
]
