# Generated by Django 3.1.4 on 2020-12-03 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201203_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users/avatars/', verbose_name='avatar'),
        ),
    ]
