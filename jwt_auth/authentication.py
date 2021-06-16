from rest_framework.authentication import BasicAuthentication
# 401 Unauthorized error for bad tokens to block access
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
# to access our default SECRET_KEY
from django.conf import settings
import jwt

# This will decode the encrypted JWT
User = get_user_model()

class JWTAuthentication(BasicAuthentication):
    def authenticate(self, request):
        # use .get() to check for whether the Authorization token exists
        # if it exists, store in header
        header = request.headers.get('Authorization')
        # if you have not supplied a token at all
        if not header:
            return None
        # if your token is does not start with Bearer
        if not header.startswith('Bearer'):
            # overwrite the permission denied message with custom message
            raise PermissionDenied({'detail': 'Invalid Authorization Header'})
        # if reached here, user has provided a Bearer Token
        # strip out the word Bearer and the space to extract the token only
        token = header.replace('Bearer ', '')

        # decode the token
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # lookup user
            # should have a key called subject which should be the user's ID 
            user = User.objects.get(pk=payload.get('sub'))
        # either the token didn't decode
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied({'detail': 'Invalid Token'})
        # couldn't find the user
        except User.DoesNotExist:
            raise PermissionDenied({'detail': 'User not Found'})
        # make the user available in all views as the request.user. 
        # request.user can then be used to check for permissions
        # tuple
        return (user, token)