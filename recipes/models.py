from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from recipes.utils import step_image_upload_to, recipe_image_upload_to


class Chef(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField('Recipe', related_name='likes', blank=True)
    bookmarks = models.ManyToManyField('Recipe', related_name='bookmarks', blank=True)

    def __str__(self):
        return self.user.username


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_('title'), max_length=64)
    author = models.ForeignKey(Chef, on_delete=models.DO_NOTHING)
    publication_time = models.DateTimeField(_('publication time'), default=timezone.now)
    cooking_time = models.DurationField(_('cooking time'))
    servings = models.SmallIntegerField(_('number of servings'))
    description = models.TextField(_('description'))

    @property
    def likes_number(self):
        return self.likes.count()

    @property
    def bookmarks_number(self):
        return self.bookmarks.count()

    def __str__(self):
        return f'{self.author}:{self.title}/{self.publication_time :%c}'


class RecipeImage(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, related_name='images', on_delete=models.CASCADE, default=None)
    image = models.ImageField(_('recipe image'), upload_to=recipe_image_upload_to, blank=True)


class Step(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE, default=None)
    description = models.TextField(_('description'))
    image = models.ImageField(_('image'), upload_to=step_image_upload_to, blank=True)


class Product(models.Model):
    UNIT_CHOICES = [
        (_('Volume'), (
            ('TSP', _('teaspoon')),
            ('TBL', _('tablespoon')),
            ('OZ', _('fluid ounce')),
            ('C', _('cup')),
            ('PT', _('pint')),
            ('QT', _('quart')),
            ('GAL', _('gallon')),
            ('ML', _('milliliter')),
            ('L', _('liter'))
        )
         ),
        (_('Mass and Weight'), (
            ('LB', _('pound')),
            ('OZ', _('ounce')),
            ('G', _('gram')),
            ('KG', _('kilogram'))
        )
         ),
        (_('Length'), (
            ('MM', _('millimeter')),
            ('CM', _('centimeter')),
            ('M', _('meter')),
            ('IN', _('inch'))
        )
         ),
        ('PI', _('piece')),
    ]
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, related_name='products', on_delete=models.CASCADE, default=None)
    name = models.CharField(_('name'), max_length=64)
    amount = models.DecimalField(_('amount'), max_digits=8, decimal_places=2,
                                 validators=[MinValueValidator(0.0)])
    unit = models.CharField(_('unit'), choices=UNIT_CHOICES, max_length=64, blank=True)


class Nutrition(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.OneToOneField(Recipe, related_name='nutrition', on_delete=models.CASCADE, default=None)
    calories = models.DecimalField(_('calories'), max_digits=8, decimal_places=2,
                                   validators=[MinValueValidator(0.0)])
    protein = models.DecimalField(_('protein'), max_digits=6, decimal_places=2,
                                  validators=[MinValueValidator(0.0)])
    carbohydrates = models.DecimalField(_('carbohydrates'), max_digits=6, decimal_places=2,
                                        validators=[MinValueValidator(0.0)])
    fat = models.DecimalField(_('carbohydrates'), max_digits=6, decimal_places=2,
                              validators=[MinValueValidator(0.0)])
