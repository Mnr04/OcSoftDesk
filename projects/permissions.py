from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Allows read only access to everyone.
    Only the author can edit or delete the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        return False


class IsProjectContributor(BasePermission):
    """
    Checks if the user is a contributor or the author of the project.
    """
    def has_object_permission(self, request, view, obj):
        from projects.models import Project, Issue, Comment

        project_concerne = None

        if isinstance(obj, Project):
            project_concerne = obj

        elif isinstance(obj, Issue):
            project_concerne = obj.project

        elif isinstance(obj, Comment):
            project_concerne = obj.issue.project

        if project_concerne is None:
            return False

        if project_concerne.author == request.user:
            return True

        if project_concerne.contributor_set.filter(user=request.user).exists():
            return True
        return False
