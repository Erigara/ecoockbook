from django.db.models import F
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ecookbook.utils import RelatedHyperlink
from recipes.models import Recipe, Nutrition, Step, RecipeImage, Product, Chef, Like, Category, CookingTime


class ChefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chef
        fields = ['url', 'user', 'likes']
        read_only_fields = ['url', 'user']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    recipes = serializers.HyperlinkedRelatedField(
        view_name='category-recipes',
        read_only=True,
        source='*'
    )

    class Meta:
        model = Category
        fields = ['url', 'name', 'image', 'recipes']
        read_only_fields = ['url']


class CookingTimeSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        hours = attrs.get('hours')
        minutes = attrs.get('minutes')
        need_preparation = attrs.get('need_preparation', False)
        preparation_hours = attrs.get('preparation_hours')
        preparation_minutes = attrs.get('preparation_minutes')
        if hours == 0 and minutes == 0:
            raise ValidationError({'hours': _('Cooking time should be greater than 0'),
                                   'minutes': _('Cooking time should be greater than 0')})
        if need_preparation and preparation_minutes == 0 and preparation_hours == 0:
            raise ValidationError({'need_preparation': _('If need preparation selected, '
                                                         'than preparation time should be greater than 0')})
        return attrs

    class Meta:
        model = CookingTime
        fields = ['hours', 'minutes', 'need_preparation', 'preparation_hours', 'preparation_minutes']


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = ['calories', 'protein', 'carbohydrates', 'fat']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    url = RelatedHyperlink(
        view_name='recipe-product-detail',
        lookup_fields=['recipe.pk', 'pk'],
        lookup_url_kwargs=['recipe', 'pk'],
        source='*',
        read_only=True
    )

    class Meta:
        model = Product
        fields = ['url', 'name', 'amount', 'unit']


class RecipeImageSerializer(serializers.HyperlinkedModelSerializer):
    url = RelatedHyperlink(
        view_name='recipe-image-detail',
        lookup_fields=['recipe.pk', 'pk'],
        lookup_url_kwargs=['recipe', 'pk'],
        source='*',
        read_only=True,
    )

    def update(self, instance: RecipeImage, validated_data):
        # delete previous image before uploading new one
        if 'image' in validated_data:
            instance.image.delete(save=False)
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = RecipeImage
        fields = ['url', 'image']


class StepSerializer(serializers.HyperlinkedModelSerializer):
    url = RelatedHyperlink(
        view_name='recipe-step-detail',
        lookup_fields=['recipe.pk', 'pk'],
        lookup_url_kwargs=['recipe', 'pk'],
        source='*',
        read_only=True
    )
    move = RelatedHyperlink(
        view_name='recipe-step-detail-move',
        lookup_fields=['recipe.pk', 'pk'],
        lookup_url_kwargs=['recipe', 'pk'],
        source='*',
        read_only=True
    )

    def create(self, validated_data):
        recipe = validated_data.get('recipe')

        # TODO Handle order
        instance = super().create(validated_data)
        return instance

    def update(self, instance: Step, validated_data):
        recipe = validated_data.get('recipe')
        # delete previous image before uploading new one
        if 'image' in validated_data:
            instance.image.delete(save=False)

        # TODO Handle order

        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Step
        fields = ['url', 'description', 'image', 'order', 'move']
        read_only_fields = ['order']


class MoveStepSerializer(serializers.Serializer):
    order = serializers.IntegerField()

    def validate_order(self, value):
        if value < 0:
            raise ValidationError('Order must be positve number')

        if value > Step.objects.current_order(self.context['recipe']):
            raise ValidationError('Order must be positve number')

        return value

class LikeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='recipe-like',
        lookup_url_kwarg='recipe',
        lookup_field='recipe_id'
    )
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        source='chef.user',
        read_only=True
    )
    recipe = serializers.HyperlinkedRelatedField(
        view_name='recipe-detail',
        read_only=True
    )
    likes_amount = serializers.IntegerField(source='recipe.likes_amount', read_only=True)

    def create(self, validated_data) -> Like:
        recipe = validated_data.get('recipe')
        chef = validated_data.get('chef')

        if Like.objects.filter(recipe=recipe, chef=chef).count() == 0:
            like = Like.objects.create(
                recipe=recipe,
                chef=chef
            )
        else:
            raise ValidationError(_('already set'))

        return like

    class Meta:
        model = Like
        fields = [
            'url',
            'recipe',
            'user',
            'has_like',
            'likes_amount',
            'creation_time',
        ]
        read_only_fields = ['url', 'creation_time']


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    like = serializers.HyperlinkedRelatedField(
        view_name='recipe-like',
        lookup_url_kwarg='recipe',
        read_only=True,
        source='id'
    )
    author = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        source='author.user',
        read_only=True
    )
    nutrition = NutritionSerializer()
    cooking_time = CookingTimeSerializer()
    products = ProductSerializer(many=True, read_only=True)
    images = RecipeImageSerializer(many=True, read_only=True)
    steps = StepSerializer(many=True, read_only=True)

    def validate(self, attrs):
        published = attrs.get('published')
        if published:
            if self.instance.steps.count() < 3:
                raise ValidationError({'steps': _('Number of steps in recipe is too low. Add at least 3 steps.')})
            if self.instance.images.count() < 1:
                raise ValidationError({'images': _('Add at least 1 image of the dish.')})
            if self.instance.products.count() < 1:
                raise ValidationError({'products': _('Add at least 1 product.')})
        return attrs

    def create(self, validated_data):
        nutrition_data = validated_data.pop('nutrition', None)
        cooking_time_data = validated_data.pop('cooking_time', None)

        recipe = Recipe.objects.create(**validated_data)

        if nutrition_data:
            nutrition_data |= {'recipe': recipe}
            serializer = NutritionSerializer()
            serializer.create(nutrition_data)

        if cooking_time_data:
            cooking_time_data |= {'recipe': recipe}
            serializer = CookingTimeSerializer()
            serializer.create(cooking_time_data)

    def update(self, instance: Recipe, validated_data):
        nutrition_data = validated_data.pop('nutrition', None)
        cooking_time_data = validated_data.pop('cooking_time', None)

        recipe = instance
        recipe = super().update(recipe, validated_data)

        if nutrition_data:
            nutrition_data |= {'recipe': recipe}
            serializer = NutritionSerializer()
            if hasattr(recipe, 'nutrition'):
                serializer.update(recipe.nutrition, nutrition_data)
            else:
                serializer.create(nutrition_data)

        if cooking_time_data:
            cooking_time_data |= {'recipe': recipe}
            serializer = CookingTimeSerializer()
            if hasattr(recipe, 'cooking_time'):
                serializer.update(recipe.cooking_time, cooking_time_data)
            else:
                serializer.create(cooking_time_data)

        return recipe

    class Meta:
        model = Recipe
        fields = [
            'url',
            'like',
            'title',
            'published',
            'category',
            'author',
            'publication_time',
            'servings',
            'description',
            'cooking_time',
            'nutrition',
            'products',
            'images',
            'steps',
        ]
        read_only_fields = ['url', 'publication_time', 'author']
