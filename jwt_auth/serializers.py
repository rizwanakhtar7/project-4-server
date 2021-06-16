# validate whether the password and password confirmation match
# hash the passwords before saving

from rest_framework import serializers
from django.contrib.auth import get_user_model
# extra validation checks for password strength which we'll comment out in DEV
# import django.contrib.auth.password_validation as validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # hide password from read views and only acknowledge in write requests
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    # must be called validate for the serializer to know what it's used for
    # data is the incoming request object
    def validate(self, data):

        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        if password != password_confirmation:
            raise ValidationError({'password_confirmation': 'does not match'})

        # EXTRA VALIDATION:
        # try:
        #     validation.validate_password(password=password)
        # except ValidationError as err:
        #     raise ValidationError({'password': err.messages})

        # hash password
        # re-attach to the data dictionary and return it
        data['password'] = make_password(password)

        return data

    class Meta:
        model = User
        fields = '__all__'