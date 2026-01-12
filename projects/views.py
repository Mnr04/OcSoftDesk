from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Issue
from .serializers import ProjectSerializer, IssueSerializer
from .permissions import IsAuthorOrReadOnly, IsProjectContributor

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
