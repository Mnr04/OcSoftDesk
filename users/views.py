from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsCurrentUser
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Manages user registration and profile updates.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Allows anyone to sign up.
        Requires authentication for other actions.
        Only the user can update or delete their own account.
        """
        permission_classes = []

        if self.action == 'create':
            permission_classes = [AllowAny()]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated(), IsCurrentUser()]

        else:
            permission_classes = [IsAuthenticated()]

        return permission_classes