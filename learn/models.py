from django.db import models
# from django.db.models.deletion import CASCADE

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=350)
    course_image = models.CharField(max_length=250)
    SubjectType = models.TextChoices('SubjectType', 'Computing, Math, Science, English')
    name = models.CharField(max_length=60)
    subject = models.CharField(blank=True, choices=SubjectType.choices, max_length=10)

    def __str__(self):
        return f'{self.title}'


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=350)
    content = models.TextField(max_length=350)
    file_upload = models.CharField(max_length=250)
    video_link = models.CharField(max_length=250)

    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Lesson {self.id} for Course {self.course}'


class Comment(models.Model):
    content = models.TextField(max_length=250)

    lesson = models.ForeignKey(
        Lesson,
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Comment {self.id} on {self.lesson}'


class Assessment(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'