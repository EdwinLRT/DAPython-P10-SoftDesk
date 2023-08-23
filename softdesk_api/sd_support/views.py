from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Project, Issue, Comment
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsProjectContributor
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 2  # Nombre d'éléments par page
    page_size_query_param = 'page_size'  # Paramètre pour spécifier la taille de la page



class ProjectViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    pagination_class = CustomPagination

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

    permission_classes = [IsAuthenticated]

class IssueViewset(ModelViewSet):
    """ View to manage Issues of a project """
    serializer_class = IssueSerializer
    pagination_class = CustomPagination
    lookup_field = 'project__slug'

    def get_queryset(self):
        project_slug = self.kwargs["project_slug"]
        return Issue.objects.filter(project__slug=project_slug)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_slug"] = self.kwargs["project_slug"]
        return context

    def perform_create(self, serializer):
        project = get_object_or_404(Project, slug=self.kwargs["project_slug"])
        serializer.save(author=self.request.user, project=project)

    permission_classes = [IsAuthenticated, IsProjectContributor]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_issue(self):
        project_slug = self.kwargs["project_slug"]
        issue_id = self.kwargs["issue_pk"]
        print(project_slug, issue_id)
        return get_object_or_404(Issue, project__slug=project_slug, id=issue_id)

    def get_queryset(self):
        issue = self.get_issue()
        return Comment.objects.filter(issue=issue)

    def perform_create(self, serializer):
        issue = self.get_issue()
        serializer.save(author=self.request.user, issue=issue)

    permission_classes = [IsAuthenticated, IsProjectContributor]
