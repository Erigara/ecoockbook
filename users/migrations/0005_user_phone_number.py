# Generated by Django 3.1.4 on 2020-12-03 11:31

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+78005553535', max_length=128, region=None, unique=True, verbose_name='phone number'),
            preserve_default=False,
        ),
    ]