# Generated by Django 4.0.2 on 2022-03-14 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_alter_question_min'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('min', models.PositiveIntegerField(default=35)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='min',
        ),
    ]
