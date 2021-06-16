from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Assessment, Course, Comment
from .serializers import (
    CourseSerializer,
    PopulatedCourseSerializer,
    AssessmentSerializer,
    CommentSerializer
)

class AssessmentDetailView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, _request, assessment_pk):

        assessments = Assessment.objects.get(pk=assessment_pk)
        serialized_assessments = AssessmentSerializer(assessments, many=True)
        return Response(serialized_assessments.data, status=status.HTTP_200_OK)


class CourseListView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, _request):
        courses = Course.objects.all()
        serialized_courses = PopulatedCourseSerializer(courses, many=True)
        return Response(serialized_courses.data, status=status.HTTP_200_OK)


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
        course = self.get_course(pk=pk)
        query = request.GET.items()

        print(list(query))
        serialized_course = PopulatedCourseSerializer(course)
        return Response(serialized_course.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        course_to_update = self.get_course(pk=pk)
        updated_course = CourseSerializer(course_to_update, data=request.data)
        if updated_course.is_valid():
            updated_course.save()
            return Response(updated_course.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_course.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        course_to_delete = self.get_course(pk=pk)
        course_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, _request):
        lessons = Course.objects.all()
        serialized_lessons = PopulatedCourseSerializer(lessons, many=True)
        return Response(serialized_lessons.data, status=status.HTTP_200_OK)

    def post(self, request, lesson_pk):
        request.data['lesson'] = lesson_pk
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


    def delete(self, _request, comment_pk):
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            raise NotFound()