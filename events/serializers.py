from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Event, RSVP, Review, UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["full_name", "bio", "location", "profile_picture"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]


class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    invitees = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), required=False
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "organizer",
            "location",
            "start_time",
            "end_time",
            "is_public",
            "invitees",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        start = attrs.get("start_time") or getattr(self.instance, "start_time", None)
        end = attrs.get("end_time") or getattr(self.instance, "end_time", None)
        if start and end and start >= end:
            raise serializers.ValidationError(
                {"end_time": "End time must be after start time."}
            )
        return attrs

    def create(self, validated_data):
        invitees = validated_data.pop("invitees", [])
        event = Event.objects.create(
            organizer=self.context["request"].user, **validated_data
        )
        if invitees:
            event.invitees.set(invitees)
        return event

    def update(self, instance, validated_data):
        invitees = validated_data.pop("invitees", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if invitees is not None:
            instance.invitees.set(invitees)
        return instance


class RSVPSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = RSVP
        fields = ["id", "event", "user", "status", "responded_at"]
        read_only_fields = ["event", "user", "responded_at"]

    def create(self, validated_data):
        request = self.context["request"]
        event = self.context["event"]
        return RSVP.objects.create(event=event, user=request.user, **validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "event", "user", "rating", "comment", "created_at"]
        read_only_fields = ["event", "user", "created_at"]

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        event = self.context["event"]
        return Review.objects.create(event=event, user=request.user, **validated_data)

