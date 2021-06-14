from rest_framework import serializers
from .models import Assessment, Comment, Course, Lesson, Question, Answer

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


class PopulatedCourseSerializer(CourseSerializer):
    lessons = PopulatedLessonSerializer(many=True)