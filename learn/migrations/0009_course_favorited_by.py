# Generated by Django 3.2.4 on 2021-06-20 13:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learn', '0008_auto_20210620_0423'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='favorited_by',
            field=models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]