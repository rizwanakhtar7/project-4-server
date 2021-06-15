from django.urls import path
from .views import CourseDetailView, CourseListView, AssessmentDetailView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/assessments/<int:assessment_pk>/', AssessmentDetailView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view())
]

