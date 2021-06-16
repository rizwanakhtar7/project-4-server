from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.db.models.fields import EmailField
from django.core.validators import MinValueValidator, MaxValueValidator

# we can override existing user fields here and add new ones
class User(AbstractUser): 
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=250)
    badge_image = models.CharField(max_length=250, blank=True)
    bio = models.TextField(max_length=350, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default = 0)
    LEARNER = 'LRN'
    INSTRUCTOR = 'INS'
    USER_TYPE = [
        (LEARNER, 'Learner'),
        (INSTRUCTOR, 'Instructor')
    ]
    role = models.CharField(
        max_length = 3,
        choices = USER_TYPE
    )

    def is_upperclass(self):
        return f'Role: {self.role}'

# class UserType(models.Model):
#     user = models.OneToOneField(
#         User,
#         related_name="type",
#         on_delete=models.CASCADE
#     )
#     LEARNER = 'LRN'
#     INSTRUCTOR = 'INS'
#     USER_TYPE = [
#         (LEARNER, 'Learner'),
#         (INSTRUCTOR, 'Instructor')
#     ]
#     role = models.CharField(
#         max_length = 3,
#         choices = USER_TYPE
#     )

#     def is_upperclass(self):
        return f'Role: {self.role}'
    # rating = models.IntegerChoices(
    #     POOR = 1,
    #     OK = 2,
    #     FAIR = 3,
    #     GREAT = 4,
    #     EXCELLENT = 4
    # )
    # rating = models.IntegerField(choices=User.choices)


# is_admin
# is_instructor
# is_learner