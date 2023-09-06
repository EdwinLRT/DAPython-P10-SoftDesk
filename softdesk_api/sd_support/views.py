from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import status
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from sd_accounts.models import CustomUser

from .models import Project, Issue, Comment, Contributor
from .permissions import IsProjectAuthor, IsContributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'


class ProjectViewset(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    pagination_class = CustomPagination
    permission_classes = [IsProjectAuthor]
    def get_queryset(self):
        queryset = Project.objects.all()
        print("Queryset : ", queryset)
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
            project_name = serializer.validated_data.get("name", "")  # assuming you have a name field
            unique_slug = self._generate_unique_slug(project_name)
            try:
                project = serializer.save(author=self.request.user, slug=unique_slug)
                contributor = Contributor.objects.create(user=self.request.user, project=project, permission='Creator')
                print("Project author set : ", contributor)
            except IntegrityError:
                raise ValidationError("Erreur lors de la création du projet. Veuillez réessayer.")
        else:
            raise ValidationError("Vous devez être connecté pour créer un projet.")

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsProjectAuthor]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def _generate_unique_slug(self, project_name):
        """Generate a unique slug for a given project name."""
        slug = slugify(project_name)
        unique_slug = slug
        num = 1
        while Project.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def destroy(self, request, *args, **kwargs):
        print("kwargs:", self.kwargs)
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


class ContributorViewset(ModelViewSet):
    """ View to manage Contributors of a project """
    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthor, IsContributor]

    def get_queryset(self):
        project_slug = self.kwargs.get("project_slug", None)
        if project_slug is None:
            return Contributor.objects.none()
        return Contributor.objects.filter(project__slug=project_slug)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, slug=self.kwargs["project_slug"])
        if not Contributor.objects.filter(user=self.request.user,
                                          project=project).exists() and project.author != self.request.user:
            raise ValidationError("Vous n'avez pas la permission d'ajouter des contributeurs.")
        username = self.request.data.get('user')
        if not username:
            raise ValidationError("Le champ 'username' est requis.")
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise ValidationError("L'utilisateur spécifié n'existe pas.")

        if Contributor.objects.filter(user=user, project=project).exists():
            raise ValidationError("L'utilisateur est déjà un contributeur de ce projet.")

        serializer.save(user=user, project=project, permission='Contributor')

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsProjectAuthor]
        elif self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsProjectAuthor | IsContributor]
        else:
            permission_classes = [IsProjectAuthor]
        return [permission() for permission in permission_classes]


class IssueViewset(ModelViewSet):
    """ View to manage Issues of a project """
    serializer_class = IssueSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'
    permission_classes = [IsProjectAuthor, IsContributor]

    def get_queryset(self):
        project_slug = self.kwargs.get("project_slug", None)
        return Issue.objects.filter(project__slug=project_slug)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_slug"] = self.kwargs.get("project_slug", None)
        return context

    def perform_create(self, serializer):
        project = get_object_or_404(Project, slug=self.kwargs["project_slug"])
        serializer.save(author=self.request.user, project=project)

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsProjectAuthor | IsContributor]
        else:
            permission_classes = [IsProjectAuthor]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    permission_classes = [IsProjectAuthor | IsContributor]

    def get_issue(self):
        project_slug = self.kwargs.get("project_slug", None)
        issue_id = self.kwargs.get("issue_id", None)
        if project_slug is None or issue_id is None:
            return None
        print("Issue id : ", issue_id)
        return get_object_or_404(Issue, project__slug=project_slug, id=issue_id)

    def get_queryset(self):
        issue = self.get_issue()
        return Comment.objects.filter(issue=issue)

    def perform_create(self, serializer):
        issue = self.get_issue()

        serializer.save(author=self.request.user, issue=issue)

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsProjectAuthor | IsContributor]
        else:
            permission_classes = [IsProjectAuthor]
        return [permission() for permission in permission_classes]
