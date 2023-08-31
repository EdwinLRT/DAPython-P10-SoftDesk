from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow user to delete his own account or admin to delete any account
    """
    def has_object_permission(self, request, view, obj):
        # if user is admin, he can delete any account
        if request.user.is_admin:
            return True
        # user can delete his own account
        return obj == request.user or obj == request.user.customuser


class CustomUserViewset(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        if request.user.is_admin:
            queryset = self.queryset
        else:
            queryset = CustomUser.objects.filter(id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
