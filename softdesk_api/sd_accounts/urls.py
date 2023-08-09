from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from .views import CustomUserViewset

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewset, basename='project')

urlpatterns = [
    path('', include(router.urls)),
    # Obtention du token d'accès
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Rafraîchissement du token d'accès
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('users/register/', CustomUserCreateView.as_view(), name='register'),
    #path('users/<int:pk>/delete/', CustomUserDeleteView.as_view(), name='user-delete'),

]
