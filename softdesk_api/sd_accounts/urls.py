from django.urls import path, include
from rest_framework import routers

from .views import CustomUserViewset

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewset, basename='project')

urlpatterns = [
    path('', include(router.urls)),
    # path('users/register/', CustomUserCreateView.as_view(), name='register'),
    #path('users/<int:pk>/delete/', CustomUserDeleteView.as_view(), name='user-delete'),

]