from rest_framework.viewsets import ModelViewSet
from sd_support.models import Project, Issue
from sd_support.serializers import ProjectSerializer, IssueSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.all()
        active = self.request.query_params.get('active', None)
        if active is not None:
            active = active.lower() in ('true', 'yes', '1')
            queryset = queryset.filter(active=active)
        return queryset


class IssueViewset(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
