# Generated by Django 5.1.1 on 2025-01-16 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_user_matching_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.CharField(default=0, max_length=3),
        ),
    ]
