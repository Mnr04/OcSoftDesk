from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Project, Issue, Contributor, Comment
from .serializers import ProjectSerializer, IssueSerializer, ContributorSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsProjectContributor
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(author=user) | Project.objects.filter(contributor__user=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(author=user) | Project.objects.filter(contributor__user=user)
        return Issue.objects.filter(project__in=projects)

    def perform_create(self, serializer):
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
