from django.contrib.auth import logout, login
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegistrationSerializer, LoginSerializer, UserSerializer


class RegistrationView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer


class LoginView(GenericAPIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        login(request, user)
        user_serializer = UserSerializer(self.request.user)
        response = Response(user_serializer.data)
        return response


class LogoutView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response()
        if self.request.user is not None:
            logout(request)
        return response
