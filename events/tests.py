from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from .models import Event

User = get_user_model()


class EventApiTests(APITestCase):
    def setUp(self):
        self.organizer = User.objects.create_user(username="org", password="pass123")
        self.other = User.objects.create_user(username="guest", password="pass123")
        self.client.login(username="org", password="pass123")

    def _create_event_payload(self, is_public=True):
        start = timezone.now() + timedelta(days=1)
        end = start + timedelta(hours=2)
        return {
            "title": "Test Event",
            "description": "desc",
            "location": "Online",
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "is_public": is_public,
        }

    def test_create_event(self):
        url = reverse("event-list")
        payload = self._create_event_payload()
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.first().organizer, self.organizer)

    def test_only_organizer_can_update(self):
        event = Event.objects.create(organizer=self.organizer, **self._create_event_payload())
        url = reverse("event-detail", args=[event.id])
        self.client.logout()
        self.client.login(username="guest", password="pass123")
        response = self.client.put(
            url, {**self._create_event_payload(), "title": "Hack"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
