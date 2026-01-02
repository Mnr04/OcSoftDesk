from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Project
from .serializers import ProjectSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def project_manager_view(request, pk=None):
    if pk is None:

        if request.method == 'GET':
            projects = Project.objects.all()
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

        if request.method == 'GET':
            serializer = ProjectSerializer(project)
            return Response(serializer.data)

        elif request.method == 'PUT':
            if project.author != request.user:
                return Response({"Vous n'êtes pas l'auteur"}, status=status.HTTP_403_FORBIDDEN)

            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if project.author != request.user:
                return Response({"Vous n'êtes pas l'auteur"}, status=status.HTTP_403_FORBIDDEN)

            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)