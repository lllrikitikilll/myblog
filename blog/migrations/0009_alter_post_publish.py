# Generated by Django 4.2 on 2023-05-06 00:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_comment_options_alter_post_options_post_tag_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
    ]
