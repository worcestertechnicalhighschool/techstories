# Generated by Django 5.1.2 on 2024-11-08 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_remove_profile_posts_profile_followers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.TextField(max_length=1000),
        ),
    ]
