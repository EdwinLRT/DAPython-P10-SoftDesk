from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewset

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewset, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
