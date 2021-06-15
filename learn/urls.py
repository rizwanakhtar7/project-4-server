from django.urls import path 
from .views import CommentListView, CourseDetailView, CourseListView, AssessmentListView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('<int:lesson_id>/comments/', CommentListView.as_view()),
    path('<int:lesson_id>/comments/<int:comment_id>/', CommentListView.as_view()),
    path('assessments/', AssessmentListView.as_view()),

]