from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Project, Issue, Contributor, Comment
from .serializers import ProjectSerializer, IssueSerializer, ContributorSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsProjectContributor
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Manages projects.
    Only authors and contributors can view projects.
    Only the author can update or delete a project.
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        """
        Returns only projects where the user is an author or a contributor.
        """
        user = self.request.user
        queryset = Project.objects.filter(author=user) | Project.objects.filter(contributor__user=user)
        return queryset.distinct()

    def perform_create(self, serializer):
        """
        Sets the logged-in user as the author of the project.
        """
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class IssueViewSet(viewsets.ModelViewSet):
    """
    Manages issues.
    Users must be contributors to the project to view or create issues.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(author=user) | Project.objects.filter(contributor__user=user)
        return Issue.objects.filter(project__in=projects)

    def perform_create(self, serializer):
        """
        Checks if the user is allowed to create an issue in this project.
        """
        project = serializer.validated_data.get('project')
        user = self.request.user

        if project.author == user:
            is_author = True
        else:
            is_author = False

        if project.contributor_set.filter(user=user).exists():
            is_contributor = True
        else:
            is_contributor = False

        if not is_author and not is_contributor:
            raise PermissionDenied("Vous ne pouvez pas créer d'issue pour ce projet.")

        serializer.save(author=user)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(author=user) | Project.objects.filter(contributor__user=user)
        return Contributor.objects.filter(project__in=projects)

    def perform_create(self, serializer):
        """
        Ensures than only the project author can add a new contributor.
        """
        project_id = self.request.data.get('project')
        project = get_object_or_404(Project, pk=project_id)

        if project.author != self.request.user:
            raise PermissionDenied("Il faut etre l'auteur pour ajouter un contributeur")

        serializer.save()

    def destroy(self, request, pk=None):
        contributor = get_object_or_404(Contributor, pk=pk)

        if contributor.project.author != request.user:
            raise PermissionDenied("vous ne pouvez pas supprimer ce contributor")

        contributor.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(author=user) | Project.objects.filter(contributor__user=user)
        return Comment.objects.filter(issue__project__in=projects)

    def perform_create(self, serializer):
        """
        Checks if the user is on the project before commenting.
        """

        issue = serializer.validated_data.get('issue')
        project = issue.project
        user = self.request.user

        if project.author == user:
            is_author = True
        else:
            is_author = False

        if project.contributor_set.filter(user=user).exists():
            is_contributor = True
        else:
            is_contributor = False

        if not is_author and not is_contributor:
            raise PermissionDenied("Vous ne pouvez pas commenter cette issue")

        serializer.save(author=user)
