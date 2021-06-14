from rest_framework import serializers
from .models import Comment, Course,Lesson

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class PopulatedLessonSerializer(LessonSerializer):
    comments = CommentSerializer(many=True)

class PopulatedCourseSerializer(CourseSerializer):
    lessons = PopulatedLessonSerializer(many=True)
