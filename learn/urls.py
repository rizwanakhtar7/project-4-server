from django.urls import path
from .views import CourseFavoriteView, CourseListView, CourseDetailView, LessonDetailListView,AssessmentDetailView,CommentListView,RatingListView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/favorite/', CourseFavoriteView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
    path('<int:pk>/lessons/', LessonDetailListView.as_view()),
    path('<int:pk>/lessons/<int:lesson_pk>/', LessonDetailListView.as_view()),
    path('<int:lesson_pk>/assessments/', AssessmentDetailView.as_view()),
    path('<int:lesson_pk>/comments/', CommentListView.as_view()),
    path('<int:lesson_pk>/comments/<int:comment_pk>/', CommentListView.as_view()),
    path('<int:pk>/ratings/', RatingListView.as_view()),

]