from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters,generics
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model

from .models import Assessment, Course, Comment, Lesson
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    PopulatedAssessmentSerializer,
    PopulatedCourseSerializer,
    AssessmentSerializer,
    CommentSerializer,
    QuestionSerializer,
    AnswerSerializer
)

User = get_user_model()


class CourseListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    # GET ALL COURSES
    def get(self, request):
        # if request.user.role == "LRN" or request.user.role == "INS":
        courses = Course.objects.all()
        serialized_courses = PopulatedCourseSerializer(courses, many=True)
        return Response(serialized_courses.data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_401_UNAUTHORIZED)

    # POST A NEW COURSE

    def post(self, request):
        if request.user.role == "INS":
            new_course = CourseSerializer(data=request.data)
            if new_course.is_valid():
                new_course.save()
                return Response(new_course.data, status=status.HTTP_201_CREATED)
            return Response(new_course.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CourseListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description','course_image','subject','name']


class CourseDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    # GET A SINGLE COURSE
    def get_course(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        if request.user.role == "LRN" or request.user.role == "INS":
            course = self.get_course(pk=pk)
            query = request.GET.items()
            print(list(query))
            serialized_course = PopulatedCourseSerializer(course)
            return Response(serialized_course.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk):
        if request.user.role == "INS":
            course_to_update = self.get_course(pk=pk)
            updated_course = CourseSerializer(course_to_update, data=request.data)
            if updated_course.is_valid():
                updated_course.save()
                return Response(updated_course.data, status=status.HTTP_202_ACCEPTED)
            return Response(updated_course.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        if request.user.role == "INS":
            course_to_delete = self.get_course(pk=pk)
            course_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class LessonDetailListView(APIView):
# GET A SINGLE LESSON
    def get_lesson(self, pk):
        try:
            return Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            raise NotFound()

    ### POST A LESSON on course ID
    def post(self, request, pk):
        if request.user.role == "INS":
            request.data['course'] = pk
            serialized_lesson = LessonSerializer(data=request.data)
            if serialized_lesson.is_valid():
                serialized_lesson.save()
                return Response(serialized_lesson.data, status=status.HTTP_201_CREATED)
            return Response(serialized_lesson.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)     
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    ### Delete A LESSON on course ID
    def delete(self, request, pk, lesson_pk):
        if request.user.role == "INS":
            try:
                lesson_to_delete = Lesson.objects.get(pk=lesson_pk)
                print(lesson_to_delete)
                lesson_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Lesson.DoesNotExist:
                raise NotFound()
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, pk, lesson_pk):
        if request.user.role == "INS":
            lesson_to_update = self.get_lesson(pk=lesson_pk)
            updated_lesson = LessonSerializer(lesson_to_update, data=request.data)
            if updated_lesson.is_valid():
                updated_lesson.save()
                return Response(updated_lesson.data, status=status.HTTP_202_ACCEPTED)
            return Response(updated_lesson.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AssessmentDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, assessment_pk):
        if request.user.role == "LRN" or request.user.role == "INS":
            assessments = Assessment.objects.get(pk=assessment_pk)
            serialized_assessments = AssessmentSerializer(assessments, many=True)
            return Response(serialized_assessments.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AssessmentDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    # GET ALL Assessments
    def get(self, request, lesson_pk):
        if request.user.role == "LRN" or request.user.role == "INS":
            assessments = Assessment.objects.all()
            serialized_assessments = PopulatedAssessmentSerializer(assessments, many=True)
            return Response(serialized_assessments.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    ### POST a Assessment on lesson ID
    def post(self, request, lesson_pk):
        if request.user.role == "INS":
            assesment = request.data.get('assessment')
            assesment['lesson'] = lesson_pk

            serialized_assessment = AssessmentSerializer(data=assesment)

            # One for loop that gets the question appends the assesment ID saves the question
            # then IN THE SAME FOR LOOP save the answer using that question ID this is 
            # assuming if your question and aswers have the same order.

            # request.data['lesson'] = lesson_pk
            # serialized_assessment = AssessmentSerializer(data=request.data)
            if serialized_assessment.is_valid():
                serialized_assessment.save()
                question = request.data.get('questions')
                question['assessment'] = serialized_assessment.data.get('id')
                serialized_question = QuestionSerializer(data=question)
                if serialized_question.is_valid():
                    serialized_question.save()
                    answer = request.data.get('answer')
                    answer['question'] = serialized_question.data.get('id')
                    serialized_answer = AnswerSerializer(data=answer)
                    if serialized_answer.is_valid():
                        serialized_answer.save()
                        return Response({
                            'assessment':serialized_assessment.data, 
                            'question':serialized_question.data,
                            'answer': serialized_answer.data}, 
                                status=status.HTTP_201_CREATED)
            return Response(serialized_assessment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CommentListView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if request.user.role == "LRN":
            lessons = Course.objects.all()
            serialized_lessons = PopulatedCourseSerializer(lessons, many=True)
            return Response(serialized_lessons.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, lesson_pk):
        if request.user.role == "LRN":
            request.data['lesson'] = lesson_pk
            serialized_comment = CommentSerializer(data=request.data)
            if serialized_comment.is_valid():
                serialized_comment.save()
                return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
            return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, comment_pk):
        if request.user.role == "LRN":
            try:
                comment_to_delete = Comment.objects.get(pk=comment_pk)
                comment_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            except Comment.DoesNotExist:
                raise NotFound()
        return Response(status=status.HTTP_401_UNAUTHORIZED)
