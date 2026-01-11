from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment

class ProjectSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']

class ContributorSerializer(serializers.Model.Serializer):
    author = serializers.StingRelatedFields(read_only=True)
    
    class Meta:
        model = Contributor
        fields = ['id','user','project']

class Issueserializer():
    author. = serializers.StringRelatedFields(real_only=True)