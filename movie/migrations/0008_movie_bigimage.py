# Generated by Django 4.2 on 2024-07-20 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='bigimage',
            field=models.ImageField(blank=True, null=True, upload_to='posters/'),
        ),
    ]
