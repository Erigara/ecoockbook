from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from datetime import datetime

from recipes.utils import step_image_upload_to, recipe_image_upload_to


class Nutrition(models.Model):
    calories = models.DecimalField(_('calories'), max_digits=6, decimal_places=2)
    protein = models.DecimalField(_('protein'), max_digits=4, decimal_places=2)
    carbohydrates = models.DecimalField(_('carbohydrates'), max_digits=4, decimal_places=2)
    fat = models.DecimalField(_('carbohydrates'), max_digits=4, decimal_places=2)


class Product(models.Model):
    name = models.CharField(_('name'), max_length=64)
    amount = models.DecimalField(_('amount'), max_digits=6, decimal_places=2)
    unit = models.CharField(_('unit'), max_length=64)


class Step(models.Model):
    description = models.TextField(_('description'))
    image = models.ImageField(_('image'), upload_to=step_image_upload_to, blank=True)


class RecipeImage(models.Model):
    image = models.ImageField(_('recipe image'), upload_to=recipe_image_upload_to, blank=True)

class Recipe(models.Model):
    title = models.CharField(_('title'), max_length=64)
    author = models.ForeignKey(Chef, on_delete=models.DO_NOTHING)
    publication_time = models.DateTimeField(_('publication time'), default=datetime.now(tz='utc'))
    cooking_time = models.DurationField(_('cooking time'))
    servings = models.SmallIntegerField(_('number of servings'))
    nutrition = models.OneToOneField(Nutrition, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField(_('description'))
    images = models.ForeignKey()
    steps = models.ForeignKey(Step, on_delete=models.CASCADE, blank=True)


class Chef(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
    bookmarks = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING)
