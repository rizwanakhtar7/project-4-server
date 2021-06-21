from django.contrib import admin
from .models import Answer, Assessment, Course, CourseFeedback, Lesson, Comment, Question
# Register your models here.
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Comment)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(CourseFeedback)

