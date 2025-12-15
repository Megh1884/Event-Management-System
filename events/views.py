from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Event, RSVP, Review
from .permissions import IsOrganizerOrReadOnly, PublicOrInvitedOnly
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer

User = get_user_model()


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.select_related("organizer").prefetch_related(
        "invitees", "rsvps", "reviews"
    )
    serializer_class = EventSerializer
    permission_classes = [PublicOrInvitedOnly & IsOrganizerOrReadOnly]
    filterset_fields = ["is_public", "location", "organizer"]
    search_fields = ["title", "location", "description"]
    ordering_fields = ["start_time", "created_at"]

    def perform_create(self, serializer):
        serializer.save()


class RSVPViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = RSVPSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return RSVP.objects.filter(event_id=event_id).select_related("event", "user")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["event"] = get_object_or_404(Event, pk=self.kwargs["event_id"])
        return context

    def perform_create(self, serializer):
        event = serializer.context["event"]
        if not event.is_public and not (
            event.organizer == self.request.user
            or event.invitees.filter(pk=self.request.user.pk).exists()
        ):
            raise PermissionDenied("You are not invited to this private event.")
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        if user_id and user_id != request.user.id and not request.user.is_staff:
            raise PermissionDenied("You can only update your own RSVP.")
        return super().partial_update(request, *args, **kwargs)


class ReviewViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return Review.objects.filter(event_id=event_id).select_related("user", "event")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["event"] = get_object_or_404(Event, pk=self.kwargs["event_id"])
        return context

    def perform_create(self, serializer):
        event = serializer.context["event"]
        if not event.is_public and not (
            event.organizer == self.request.user
            or event.invitees.filter(pk=self.request.user.pk).exists()
        ):
            raise PermissionDenied("You are not invited to this private event.")
        serializer.save()
