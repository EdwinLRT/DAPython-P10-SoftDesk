from rest_framework.serializers import ModelSerializer
from sd_support.models import Project, Issue


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'creation_date', 'last_modification', 'owner', 'type', 'active']

class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['author','title', 'description', 'status', 'type', 'priority', 'creation_date', 'last_modification', 'project', 'assigned_to']