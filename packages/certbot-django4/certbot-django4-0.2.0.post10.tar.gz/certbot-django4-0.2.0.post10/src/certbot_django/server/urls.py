from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"challenges", views.AcmeChallengeViewSet)


urlpatterns = [
    path(r"acme-challenge/<acme_data>", views.detail, name="acmechallenge-response"),
    path(r"", include(router.urls)),
]
