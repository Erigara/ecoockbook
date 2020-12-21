from django.db import models
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from recipes.models import Recipe, Category


@registry.register_document
class RecipeDocument(Document):
    category = fields.ObjectField(properties={
        'name': fields.TextField(),
    })
    steps = fields.NestedField(properties={
        'description': fields.TextField(),
    })
    products = fields.NestedField(properties={
        'name': fields.TextField()
    })
    nutrition = fields.NestedField(properties={
        'calories': fields.FloatField(),
        'protein': fields.FloatField(),
        'carbohydrates': fields.FloatField(),
        'fat': fields.FloatField()
    })
    cooking_time = fields.NestedField(properties={
        'hours': fields.ShortField(),
        'minutes': fields.ShortField(),
        'need_preparation': fields.BooleanField(),
        'preparation_hours': fields.ShortField(),
        'preparation_minutes': fields.ShortField()
    })
    likes_amount = fields.IntegerField()
    author = fields.TextField()

    def prepare_author(self, instance):
        return instance.author.user.username

    class Index:
        name = 'recipes'

    class Django:
        model = Recipe
        fields = [
            'title',
            'publication_time',
            'servings',
            'description',
        ]
        related_models = [Category]

    def get_queryset(self):
        """
        Только опубликованные рецепты попадают в поисковый индекс
        """
        return super(RecipeDocument, self).get_queryset().filter(published=True).select_related(
            'category',
            'author'
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Category):
            return related_instance.recipes.filter(published=True)

    def update(self, thing, refresh=None, action='index', parallel=False, **kwargs):
        """
        В индекс при update попадают только опубликованные рецепты
        """
        if isinstance(thing, models.Model):
            if not thing.published:
                thing = []
        elif isinstance(thing, models.QuerySet):
            thing = thing.filter(published=True)
        else:
            thing = [instance for instance in thing if instance.published]
        return super().update(thing, refresh, action, parallel, **kwargs)
