from rest_framework import serializers
from .models import Project, Issue, Contributor, Comment

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']

class IssueSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'issue_type', 'priority', 'status', 'project', 'author', 'created_time']

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time', 'uuid']