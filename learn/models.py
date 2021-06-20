from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.deletion import DO_NOTHING

# from django.db.models.deletion import CASCADE


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=350)
    course_image = models.CharField(max_length=250)
    SubjectType = models.TextChoices('SubjectType', 'Computing, Math, Science, English')
    name = models.CharField(max_length=60)
    subject = models.CharField(blank=True, choices=SubjectType.choices, max_length=10)
    rating_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='ratings',
        blank=True
    )
    favorited_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='favorites',
        blank=True
    )

    def __str__(self):
        return f'{self.title}'

class CourseFeedback(models.Model):

    class Ratings(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5

    rating = models.IntegerField(choices=Ratings.choices)
    user = models.ForeignKey(
        'jwt_auth.User',
        related_name="feedback",
        null=True,
        on_delete=DO_NOTHING,
    )
    course = models.ForeignKey(
        Course,
        related_name="feedback",
        on_delete=models.CASCADE

    )

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
    user = models.ForeignKey(
        'jwt_auth.User',
        related_name="comments",
        null=True,
        on_delete=DO_NOTHING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment {self.id} on {self.lesson}'


class Assessment(models.Model):
    name = models.CharField(max_length=50)
    
    lesson = models.OneToOneField(
        Lesson,
        related_name="assessment",
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return f'{self.name}-{self.lesson}'


class Question(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        related_name="questions",
        on_delete=models.CASCADE
    )
    question = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.question}'
    # correct_answers = ArrayField(models.CharField(max_length=15), null=True, blank=True)
    # incorrect_answers = ArrayField(models.CharField(max_length=15), null=True, blank=True)


class Answer(models.Model):
    answer = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(
        Question,
        related_name="answers", 
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.answer}'


class Result(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f'result: {self.score}'
