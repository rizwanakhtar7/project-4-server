from django.urls import path
from .views import CourseDetailView, CourseListView, AssessmentDetailView, CommentListView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/assessments/<int:assessment_pk>/', AssessmentDetailView.as_view()),
    path('<int:lesson_id>/comments/', CommentListView.as_view()),
    path('<int:lesson_id>/comments/<int:comment_id>/', CommentListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view())
]