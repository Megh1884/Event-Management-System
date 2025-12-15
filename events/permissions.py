from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrganizerOrReadOnly(BasePermission):
    message = "Only the organizer can modify this event."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.organizer == request.user


class PublicOrInvitedOnly(BasePermission):
    message = "This event is private; only invitees or the organizer can view."

    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        if not request.user.is_authenticated:
            return False
        return obj.organizer == request.user or obj.invitees.filter(
            pk=request.user.pk
        ).exists()

