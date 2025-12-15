from django.contrib import admin

from .models import Event, RSVP, Review, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "location")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "organizer", "start_time", "is_public")
    list_filter = ("is_public", "start_time")
    search_fields = ("title", "description", "location")
    filter_horizontal = ("invitees",)


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "status", "responded_at")
    list_filter = ("status",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "rating", "created_at")
    search_fields = ("comment",)
