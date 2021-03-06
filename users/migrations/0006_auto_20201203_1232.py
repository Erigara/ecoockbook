# Generated by Django 3.1.4 on 2020-12-03 12:32

from django.db import migrations, models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to=users.utils.avatar_upload_to, verbose_name='avatar'),
        ),
    ]
