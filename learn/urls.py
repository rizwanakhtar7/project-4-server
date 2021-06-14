from django.urls import path 
from .views import CourseDetailView, CourseListView

urlpatterns = [
    path('', CourseListView.as_view()),
    path('<int:pk>/', CourseDetailView.as_view()),
]