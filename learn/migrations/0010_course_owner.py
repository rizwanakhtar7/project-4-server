# Generated by Django 3.2.4 on 2021-06-21 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learn', '0009_course_favorited_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses_created', to='jwt_auth.user'),
            preserve_default=False,
        ),
    ]