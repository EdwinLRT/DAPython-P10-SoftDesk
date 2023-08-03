from django.urls import path, include
from rest_framework import routers

from .views import ProjectViewset, IssueViewset

router = routers.DefaultRouter()
router.register('projects', ProjectViewset, basename='project')
router.register(r'projects/(?P<project_id>\d+)/issues', IssueViewset, basename='issue')
urlpatterns = [
    path('', include(router.urls)),
]