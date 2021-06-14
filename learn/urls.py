from django.urls import path 
from .views import CourseDetailView, CourseListView, AssessmentListView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('assessments/', AssessmentListView.as_view()),

]