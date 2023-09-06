from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404

from .models import Project, Issue, Comment, Contributor


class IsProjectAuthor(BasePermission):
    message = 'Only the project author can perform this action.'

    def has_permission(self, request, view):
        print("IsProjectAuthor has_permission")
        project_slug = view.kwargs.get('project_slug') or view.kwargs.get('slug')
        print("project_slug: ", project_slug)
        project = get_object_or_404(Project, slug=project_slug)
        contributor = get_object_or_404(Contributor, user=request.user, project=project)

        if contributor.permission == 'Creator':
            print("IsProjectAuthor has_permission: True")
            return True
        print("IsProjectAuthor has_permission: False")
        return False

    def has_object_permission(self, request, view, obj):
        print("IsProjectAuthor has_object_permission")
        if isinstance(obj, Project):
            return Contributor.objects.filter(user=request.user, project=obj, permission='Creator').exists()
        return False


class IsContributor(BasePermission):
    message = 'You must be a contributor to perform this action.'

    def has_permission(self, request, view):
        print("IsContributor has_permission")
        project_slug = view.kwargs.get('project_slug') or view.kwargs.get('slug')
        project = get_object_or_404(Project, slug=project_slug)

        is_contributor = Contributor.objects.filter(user=request.user, project=project).exists()
        if is_contributor:
            print("IsContributor has_permission: True")
            return True

        return False

    def has_object_permission(self, request, view, obj):
        print("IsContributor has_object_permission")
        print(request.user)
        print(obj)

        if isinstance(obj, Project):
            print("Obj is Project")
            return Contributor.objects.filter(user=request.user, project=obj).exists()

        elif isinstance(obj, Issue):
            print("Obj is Issue")
            project = obj.project
            return Contributor.objects.filter(user=request.user, project=project).exists()

        elif isinstance(obj, Comment):
            print("Obj is Comment")
            issue = obj.issue  # Suppose que Comment a un champ 'issue' lié à l'Issue
            project = issue.project  # On obtient le projet via l'Issue
            return Contributor.objects.filter(user=request.user, project=project).exists()

        return False

