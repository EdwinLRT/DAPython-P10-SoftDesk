from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from sd_accounts.models import CustomUser
from sd_support.models import Project, Issue, Comment, Contributor


class ProjectSerializer(ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Project
        fields = ['id', 'slug', 'name', 'description', 'author', 'creation_date', 'last_modification', 'type', 'active']


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


class ContributorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    project = serializers.SlugRelatedField(slug_field='slug', queryset=Project.objects.all(), required=False)

    class Meta:
        model = Contributor
        fields = '__all__'
        read_only_fields = ('project', 'role', 'id')
