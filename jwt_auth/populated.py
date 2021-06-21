from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from learn.serializers import CourseSerializer
from learn.serializers import CommentSerializer

User = get_user_model()

class PopulatedUserSerializer(ModelSerializer):
    favorites = CourseSerializer(many=True)
    # comments = CommentSerializer(many=True)
    # created_courses = CourseSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'profile_image',
            'email',
            'favorites',
        )