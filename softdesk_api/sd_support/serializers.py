from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from sd_support.models import Project, Issue

class ProjectSerializer(ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Project
        fields = ['id', 'slug', 'name', 'description', 'owner', 'creation_date', 'last_modification', 'type', 'active']

class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'slug', 'author', 'title', 'description', 'status', 'type', 'priority', 'creation_date', 'last_modification', 'project', 'assigned_to']
