# time required for token issue time and expiry
from datetime import datetime, timedelta
from jwt_auth.populated import PopulatedUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# in case something goes wrong with login
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
# so we can look up the user once they login
from django.contrib.auth import get_user_model
# the secret so we can encode them with the secret
from django.conf import settings
import jwt

from .serializers import UserSerializer

User = get_user_model()


class RegisterView(APIView):

    def post(self, request):
        user_to_create = UserSerializer(data=request.data)
        if user_to_create.is_valid():
            user_to_create.save()
            return Response(
                {'message: Registration Succesfull'},
                status=status.HTTP_201_CREATED
            )
        return Response(user_to_create.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class LoginView(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_to_login = User.objects.get(email=email)
        # do not give clues as to why they couldn't login
        except User.DoesNotExist:
            raise PermissionDenied({'detail': 'Unauthorized'})

        if not user_to_login.check_password(password):
            raise PermissionDenied({'detail': 'Unauthorized'})

        expiry_time = datetime.now() + timedelta(days=7)
        token = jwt.encode(
            {'sub': user_to_login.id, 'exp':  int(expiry_time.strftime('%s'))},
            settings.SECRET_KEY,
            algorithm='HS256'
        )
        return Response(
            {'token': token, 'message': f'Welcome back {user_to_login.username}'}
        )

class ProfileView(APIView):

    def get(self, _request, pk):
        try:
            user = User.objects.get(pk=pk)
            serialized_user = UserSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise NotFound()