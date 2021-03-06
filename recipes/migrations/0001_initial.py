# Generated by Django 3.1.4 on 2020-12-20 13:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ecookbook.utils
import functools
import recipes.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='category title')),
                ('image', models.ImageField(blank=True, upload_to=functools.partial(ecookbook.utils.specific_upload_to, *(), **{'path': recipes.utils.category_path}), verbose_name='category image')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='title')),
                ('publication_time', models.DateTimeField(blank=True, null=True, verbose_name='publication time')),
                ('published', models.BooleanField(default=False, verbose_name='published')),
                ('servings', models.SmallIntegerField(verbose_name='number of servings')),
                ('description', models.TextField(verbose_name='description')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='own_recipes', to='recipes.chef')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to='recipes.category')),
            ],
            options={
                'ordering': ['publication_time'],
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.PositiveSmallIntegerField(verbose_name='order')),
                ('description', models.TextField(verbose_name='description')),
                ('image', models.ImageField(blank=True, upload_to=functools.partial(ecookbook.utils.specific_upload_to, *(), **{'path': recipes.utils.step_path}), verbose_name='step image')),
                ('recipe', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='recipes.recipe')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='RecipeImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, upload_to=functools.partial(ecookbook.utils.specific_upload_to, *(), **{'path': recipes.utils.recipe_image_path}), verbose_name='recipe image')),
                ('recipe', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='recipes.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='amount')),
                ('unit', models.CharField(blank=True, choices=[('Volume', (('TSP', 'teaspoon'), ('TBL', 'tablespoon'), ('OZ', 'fluid ounce'), ('C', 'cup'), ('PT', 'pint'), ('QT', 'quart'), ('GAL', 'gallon'), ('ML', 'milliliter'), ('L', 'liter'))), ('Mass and Weight', (('LB', 'pound'), ('OZ', 'ounce'), ('G', 'gram'), ('KG', 'kilogram'))), ('Length', (('MM', 'millimeter'), ('CM', 'centimeter'), ('M', 'meter'), ('IN', 'inch'))), ('PI', 'piece')], max_length=64, verbose_name='unit')),
                ('recipe', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='recipes.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Nutrition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('calories', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='calories')),
                ('protein', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='protein')),
                ('carbohydrates', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='carbohydrates')),
                ('fat', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='carbohydrates')),
                ('recipe', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='nutrition', to='recipes.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='creation time')),
                ('chef', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.chef')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
            options={
                'unique_together': {('chef', 'recipe')},
            },
        ),
        migrations.CreateModel(
            name='CookingTime',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hours', models.SmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], verbose_name='hour(s)')),
                ('minutes', models.SmallIntegerField(choices=[(0, 0), (15, 15), (30, 30), (45, 45)], verbose_name='minute(s)')),
                ('need_preparation', models.BooleanField(default=False, verbose_name='need preparation')),
                ('preparation_hours', models.SmallIntegerField(blank=True, choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], default=0, verbose_name='preparation hour(s)')),
                ('preparation_minutes', models.SmallIntegerField(blank=True, choices=[(0, 0), (15, 15), (30, 30), (45, 45)], default=0, verbose_name='preparation minute(s)')),
                ('recipe', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='cooking_time', to='recipes.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='chef',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', through='recipes.Like', to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='chef',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
