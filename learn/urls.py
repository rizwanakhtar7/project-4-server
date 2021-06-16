from django.urls import path
from .views import CourseListView, CourseDetailView, LessonDetailListView,AssessmentDetailView,CommentListView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('<int:pk>/lessons/', LessonDetailListView.as_view()),
    path('<int:pk>/lessons/<int:lesson_pk>/', LessonDetailListView.as_view()),
    path('<int:lesson_pk>/assessments/', AssessmentDetailView.as_view()),
    path('<int:lesson_pk>/comments/', CommentListView.as_view()),
    path('<int:lesson_pk>/comments/<int:comment_pk>/', CommentListView.as_view()),
]