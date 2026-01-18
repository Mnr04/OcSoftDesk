from rest_framework import serializers
from .models import Project, Issue, Contributor, Comment


class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']

    def perform_create(self, serializer):
        """
        Sets the logged-in user as the author of the project.
        """
        serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class IssueSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'issue_type',
            'priority',
            'status',
            'project',
            'author',
            'created_time',
            'assignee'
            ]

    def validate(self, data):
        if 'project' in data:
            project = data['project']
        elif self.instance:
            project = self.instance.project
        else:
            project = None

        if 'assignee' in data:
            assignee = data['assignee']
        elif self.instance:
            assignee = self.instance.assignee
        else:
            assignee = None

        if assignee is None:
            return data

        if project is None:
            raise serializers.ValidationError("Pas de Projet")

        is_author = (project.author == assignee)
        is_contributor = project.contributor_set.filter(user=assignee).exists()

        if not is_author and not is_contributor:
            raise serializers.ValidationError({
                "L'assigné doit etre contributeur au projet"
            })

        return data


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'description', 'issue', 'author', 'created_time', 'uuid']
