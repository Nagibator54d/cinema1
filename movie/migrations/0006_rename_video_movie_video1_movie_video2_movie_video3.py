# Generated by Django 4.2 on 2024-07-20 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_remove_movie_actorphoto1_remove_movie_actorphoto2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='video',
            new_name='video1',
        ),
        migrations.AddField(
            model_name='movie',
            name='video2',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
        migrations.AddField(
            model_name='movie',
            name='video3',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
