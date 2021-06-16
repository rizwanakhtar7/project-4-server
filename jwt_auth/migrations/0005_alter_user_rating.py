# Generated by Django 3.2.4 on 2021-06-16 11:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0004_auto_20210616_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]