from rest_framework import permissions
from .models import Contributor

class IsProjectContributor(permissions.BasePermission):
    message = "Vous n'êtes pas contributeur de ce projet."

    def has_permission(self, request, view):
        project_slug = view.kwargs.get('project_slug')
        user = request.user

        if project_slug:
            return Contributor.objects.filter(project__slug=project_slug, user=user).exists()

        return False
