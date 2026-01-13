from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Issue, Contributor, Comment
from .serializers import ProjectSerializer, IssueSerializer, ContributorSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsProjectContributor
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

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
        serializer.save(author=self.request.user)

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]

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

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        projects = Project.objects.filter(author=user) | Project.objects.filter(contributor__user=user)
        return comment.objects.filter(issue__project__in=projects)

    def perform_create(self, serializer):
        serializer.save()
