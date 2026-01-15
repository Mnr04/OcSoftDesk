from rest_framework import permissions

class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        utilisateur_connecte = request.user
        utilisateur_a_modifier = obj

        if utilisateur_connecte == utilisateur_a_modifier:
            return True
        else:
            return False