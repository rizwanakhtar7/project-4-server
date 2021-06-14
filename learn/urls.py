from django.urls import path 
from .views import CourseDetailListView, CourseListView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailListView.as_view()),
]