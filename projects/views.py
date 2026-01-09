from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def project_view(request, pk=None):

    if pk is None:
        if request.method == 'GET':
            projects = Project.objects.filter(author=request.user) | Project.objects.filter(contributor__user=request.user)
            projects = projects.distinct()

            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        project = get_object_or_404(Project, pk=pk)

        is_contributor = project.contributor_set.filter(user=request.user).exists()
        if project.author != request.user and not is_contributor:
            return Response({"error": "Accès interdit"}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            serializer = ProjectSerializer(project)
            return Response(serializer.data)

        elif request.method == 'PUT':
            if project.author != request.user:
                return Response({"error": "Vous n'êtes pas l'auteur"}, status=status.HTTP_403_FORBIDDEN)

            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if project.author != request.user:
                return Response({"error": "Vous n'êtes pas l'auteur"}, status=status.HTTP_403_FORBIDDEN)

            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def contributor_view(request, pk=None):

    if pk is None:
        if request.method == 'GET':
            my_projects = Project.objects.filter(author=request.user) | Project.objects.filter(contributor__user=request.user)
            contributors = Contributor.objects.filter(project__in=my_projects).distinct()

            serializer = ContributorSerializer(contributors, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = ContributorSerializer(data=request.data)
            if serializer.is_valid():
                project = serializer.validated_data['project']
                if project.author != request.user:
                     return Response({"error": "Seul l'auteur du projet peut ajouter des contributeurs"}, status=status.HTTP_403_FORBIDDEN)

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        contributor = get_object_or_404(Contributor, pk=pk)

        is_allowed = contributor.project.author == request.user or contributor.project.contributor_set.filter(user=request.user).exists()
        if not is_allowed:
             return Response({"error": "Accès interdit"}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            serializer = ContributorSerializer(contributor)
            return Response(serializer.data)

        elif request.method == 'DELETE':
            if contributor.project.author != request.user:
                 return Response({"error": "Seul l'auteur du projet peut supprimer un contributeur"}, status=status.HTTP_403_FORBIDDEN)

            contributor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def issue_view(request, pk=None):

    if pk is None:
        if request.method == 'GET':
            my_projects = Project.objects.filter(author=request.user) | Project.objects.filter(contributor__user=request.user)
            issues = Issue.objects.filter(project__in=my_projects).distinct()

            serializer = IssueSerializer(issues, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = IssueSerializer(data=request.data)
            if serializer.is_valid():
                project = serializer.validated_data['project']
                is_contributor = project.contributor_set.filter(user=request.user).exists()
                if project.author != request.user and not is_contributor:
                     return Response({"error": "Vous devez être contributeur pour créer une issue"}, status=status.HTTP_403_FORBIDDEN)

                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        issue = get_object_or_404(Issue, pk=pk)

        is_contributor = issue.project.contributor_set.filter(user=request.user).exists()
        if issue.project.author != request.user and not is_contributor:
             return Response({"error": "Accès interdit"}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            serializer = IssueSerializer(issue)
            return Response(serializer.data)

        elif request.method == 'PUT':
            if issue.author != request.user:
                 return Response({"error": "Vous n'êtes pas l'auteur"}, status=status.HTTP_403_FORBIDDEN)

            serializer = IssueSerializer(issue, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if issue.author != request.user:
                 return Response({"error": "Vous n'êtes pas l'auteur"}, status=status.HTTP_403_FORBIDDEN)

            issue.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_view(request, pk=None):

    if pk is None:
        if request.method == 'GET':
            my_projects = Project.objects.filter(author=request.user) | Project.objects.filter(contributor__user=request.user)
            comments = Comment.objects.filter(issue__project__in=my_projects).distinct()

            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                issue = serializer.validated_data['issue']
                project = issue.project
                is_contributor = project.contributor_set.filter(user=request.user).exists()
                if project.author != request.user and not is_contributor:
                     return Response({"error": "Accès interdit"}, status=status.HTTP_403_FORBIDDEN)

                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        comment = get_object_or_404(Comment, pk=pk)

        project = comment.issue.project
        is_contributor = project.contributor_set.filter(user=request.user).exists()
        if project.author != request.user and not is_contributor:
             return Response({"error": "Accès interdit"}, status=status.HTTP_403_FORBIDDEN)

        if request.method == 'GET':
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        elif request.method == 'PUT':
            if comment.author != request.user:
                 return Response({"error": "Vous n'êtes pas l'auteur"}, status=status.HTTP_403_FORBIDDEN)

            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if comment.author != request.user:
                 return Response({"error": "Vous n'êtes pas l'auteur"}, status=status.HTTP_403_FORBIDDEN)

            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
