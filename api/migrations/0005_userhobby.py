# Generated by Django 5.1.1 on 2025-01-14 21:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.hobby')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
    ]
