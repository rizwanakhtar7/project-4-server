from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .models import Assessment, Course, Comment
from .serializers import (
    CourseSerializer,
    PopulatedCourseSerializer,
    AssessmentSerializer,
    CommentSerializer
)

User = get_user_model()

class AssessmentDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request, assessment_pk):
        if request.user.role == "LRN" or request.user.role == "INS":
            assessments = Assessment.objects.get(pk=assessment_pk)
            serialized_assessments = AssessmentSerializer(assessments, many=True)
            return Response(serialized_assessments.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class CourseListView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if request.user.role == "LRN" or request.user.role == "INS":
            courses = Course.objects.all()
            serialized_courses = PopulatedCourseSerializer(courses, many=True)
            return Response(serialized_courses.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        new_course = CourseSerializer(data=request.data)
        if new_course.is_valid():
            new_course.save()
            return Response(new_course.data,  status=status.HTTP_201_CREATED)
        return Response(new_course.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CourseDetailView(APIView):

    permission_classes = (IsAuthenticated, )
    
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