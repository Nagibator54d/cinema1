# Generated by Django 4.2 on 2024-07-21 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0012_alter_episode_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='series',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movie.series'),
            preserve_default=False,
        ),
    ]
