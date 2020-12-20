from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from recipes.utils import category_upload_to, recipe_image_upload_to, step_upload_to


class Chef(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        'Recipe',
        related_name='likes',
        through='Like',
        through_fields=('chef', 'recipe'),
        blank=True
    )

    def __str__(self):
        return self.user.username


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('category title'), unique=True, max_length=64)
    image = models.ImageField(
        _('category image'),
        upload_to=category_upload_to,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(_('title'), max_length=64)
    author = models.ForeignKey(Chef, related_name='own_recipes', on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, related_name='recipes', blank=True, null=True, on_delete=models.SET_NULL)
    publication_time = models.DateTimeField(_('publication time'), blank=True, null=True)
    published = models.BooleanField(_('published'), default=False)
    servings = models.SmallIntegerField(_('number of servings'))
    description = models.TextField(_('description'))

    @property
    def likes_amount(self):
        return self.likes.count()

    @classmethod
    def template(cls, author: Chef):
        instance = cls.objects.create(
            title=_('Your original title'),
            author=author,
            servings=4,
            description=_('Describe your dish...')
        )
        return instance

    def __str__(self):
        if self.publication_time:
            return f'{self.author}:{self.title}/{self.publication_time :%c}'
        else:
            return f'{self.author}:{self.title}/unpublished'

    class Meta:
        ordering = ['publication_time']


class RecipeImage(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, related_name='images', on_delete=models.CASCADE, default=None)
    image = models.ImageField(
        _('recipe image'),
        upload_to=recipe_image_upload_to,
        blank=True
    )



class Step(models.Model):
    id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey(Recipe, related_name='steps', on_delete=models.CASCADE, default=None)
    order = models.PositiveSmallIntegerField(_('order'))
    description = models.TextField(_('description'))
    image = models.ImageField(
        _('step image'),
        upload_to=step_upload_to,
        blank=True
    )

    class Meta:
        ordering = ['order']


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


class CookingTime(models.Model):
    hour_choices = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)]
    minutes_choices = [(0, 0), (15, 15), (30, 30), (45, 45)]
    id = models.AutoField(primary_key=True)
    recipe = models.OneToOneField(Recipe, related_name='cooking_time', on_delete=models.CASCADE, default=None)
    hours = models.SmallIntegerField(_('hour(s)'), choices=hour_choices)
    minutes = models.SmallIntegerField(_('minute(s)'), choices=minutes_choices)
    need_preparation = models.BooleanField(_('need preparation'), default=False)
    preparation_hours = models.SmallIntegerField(_('preparation hour(s)'), choices=hour_choices, default=0, blank=True)
    preparation_minutes = models.SmallIntegerField(_('preparation minute(s)'), choices=minutes_choices, default=0, blank=True)


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(_('creation time'), default=timezone.now)

    # если объект модели не сохранен в бд, то лайк ещё не стоит
    @property
    def has_like(self):
        return not self._state.adding

    class Meta:
        unique_together = ['chef', 'recipe']
