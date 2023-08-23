from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from sd_support.models import Project, Issue, Comment
from django.shortcuts import get_object_or_404


class ProjectSerializer(ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = ['id', 'slug', 'name', 'description', 'owner', 'creation_date', 'last_modification', 'type', 'active']


class IssueSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    project = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = Issue
        fields = ['id', 'author', 'title', 'description', 'status', 'type', 'priority', 'creation_date',
                  'last_modification', 'project']

    def create(self, validated_data):
        project_slug = self.context.get("project_slug")
        project = get_object_or_404(Project, slug=project_slug)
        validated_data["project"] = project
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'creation_date', 'last_modification', 'author']
