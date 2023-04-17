from rest_framework import generics, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from record.views import BaseRecordViewSet
from core.models import User
from user.serializers import (
    AuthTokenSerializer,
    UserSerializer,
)
from rest_framework.response import Response


class ListCreateUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class BalanceViewSet(BaseRecordViewSet):
    """Create a new auth token for the user."""

    def list(self, _request):
        user_balance = self.get_user_balance()
        return Response({"user_balance": user_balance})
