# Generated by Django 4.1 on 2023-04-11 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Movies', '0008_movies_director_movies_duration_movies_genre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='stars',
        ),
    ]