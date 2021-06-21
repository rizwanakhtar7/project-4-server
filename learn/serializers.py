# from learn.views import User
from rest_framework import serializers
from .models import Assessment, Comment, Course, CourseFeedback, Lesson, Question, Answer
from django.contrib.auth import get_user_model

User = get_user_model()

class CourseFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseFeedback
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username']


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


class AssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assessment
        fields = '__all__'

 
class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

class PopulatedQuestionSerializer(QuestionSerializer):
    answers = AnswerSerializer(many=True)


class PopulatedAssessmentSerializer(AssessmentSerializer):
    questions = PopulatedQuestionSerializer(many=True)


class PopulatedLessonSerializer(LessonSerializer):
    comments = CommentSerializer(many=True)
    assessment = PopulatedAssessmentSerializer()


class PopulatedCourseFeedbackSerializer(CourseFeedbackSerializer):
    user = CustomUserSerializer()

class PopulatedCourseSerializer(CourseSerializer):
    lessons = PopulatedLessonSerializer(many=True)
    rating_by = UserSerializer(many=True)
    feedback = PopulatedCourseFeedbackSerializer(many=True)
    favorited_by = CustomUserSerializer(many=True)
    owner =  UserSerializer()