from rest_framework.permissions import BasePermission, IsAuthenticated
from .models import Project, Issue, Comment

from .models import Contributor


class IsProjectAuthor(BasePermission):
    message = 'Only the project author can perform this action.'
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        print("Inside IsProjectAuthor: has_object_permission")
        if isinstance(obj, Project):
            print(f"Object is a Project: {obj.name}")
            is_author_directly = obj.author == request.user
            print(f"User is direct author: {is_author_directly}")
            is_author_via_contributor = Contributor.objects.filter(user=request.user, project=obj,
                                                                   is_author=True).exists()
            print(f"User is author via contributor: {is_author_via_contributor}")
            return is_author_directly or is_author_via_contributor
        print("Object is not a Project")
        return False


class IsContributor(BasePermission):
    message = 'You must be a contributor to perform this action.'
    def has_permission(self, request, view):
        return False
    def has_object_permission(self, request, view, obj):
        return False

    # def has_object_permission(self, request, view, obj):
    #     print("Inside IsContributor: has_object_permission")
    #     print(f"Evaluating IsContributor for user '{request.user.username}' on object '{obj.__class__.__name__}'")
    #     if isinstance(obj, Project):
    #         is_contributor = Contributor.objects.filter(user=request.user, project=obj).exists()
    #     elif isinstance(obj, (Issue, Comment)):
    #         is_contributor = Contributor.objects.filter(user=request.user, project=obj.project).exists()
    #     else:
    #         is_contributor = False
    #     print(f"Is user '{request.user.username}' a contributor of '{obj}': {is_contributor}")
    #     return is_contributor
