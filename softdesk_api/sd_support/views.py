from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sd_support.models import Project, Issue
from sd_support.serializers import ProjectSerializer, IssueSerializer

class ProjectViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Project.objects.all()
        active = self.request.query_params.get('active', None)
        if active is not None:
            active = active.lower() in ('true', 'yes', '1')
            queryset = queryset.filter(active=active)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Vous devez être connecté pour créer un projet.")

class IssueViewset(ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        serializer.save(slug=serializer.validated_data['title'])  # Assurez-vous de définir le slug ici

