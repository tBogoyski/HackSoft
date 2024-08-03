from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import CustomUser
from users.serializers import UserCreateSerializer, UserSerializer


class RegisterUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserProfileView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.filter(is_valid=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self) -> 'CustomUser':
        return self.request.user
