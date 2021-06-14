from rest_framework.exceptions import NotFound
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import serializers, status

from .models import Assessment, Course, Lesson
from .serializers import CourseSerializer,LessonSerializer,PopulatedCourseSerializer,PopulatedLessonSerializer, AssessmentSerializer

class AssessmentListView(APIView):
    
    def get(self, _request):
        assessments = Assessment.objects.all()
        serialized_assessments = AssessmentSerializer(assessments, many=True)
        return Response(serialized_assessments.data, status=status.HTTP_200_OK)


class CourseListView(APIView):

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
    def get_course(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise NotFound()

    def get(self, _request, pk):
        course = self.get_course(pk=pk)
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

