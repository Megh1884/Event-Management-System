from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, RSVPViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "events/<int:event_id>/rsvp/",
        RSVPViewSet.as_view({"post": "create"}),
        name="event-rsvp",
    ),
    path(
        "events/<int:event_id>/rsvp/<int:pk>/",
        RSVPViewSet.as_view({"patch": "partial_update"}),
        name="event-rsvp-update",
    ),
    path(
        "events/<int:event_id>/reviews/",
        ReviewViewSet.as_view({"get": "list", "post": "create"}),
        name="event-reviews",
    ),
]

