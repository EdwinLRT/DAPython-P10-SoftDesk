from django.urls import path, include
from .views import ProjectViewset, IssueViewset, CommentViewSet, ContributorViewset
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewset, basename='project')

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register('users', ContributorViewset, basename="project-users")
projects_router.register(r'issues', IssueViewset, basename='project-issue')

issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),

]
