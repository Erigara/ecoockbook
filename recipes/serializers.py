from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Recipe, Nutrition, Step, RecipeImage, Product, Chef, Like


class ChefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chef
        fields = ['url', 'user', 'likes']
        read_only_fields = ['url', 'user']


class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = ['calories', 'protein', 'carbohydrates', 'fat']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'amount', 'unit']


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
        fields = ['image']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['description', 'image']


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='like-detail',
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


# TODO обработка вложенных серилизаторов
class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    like = serializers.HyperlinkedRelatedField(
        view_name='like-detail',
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
    products = ProductSerializer(many=True)
    images = RecipeImageSerializer(many=True)
    steps = StepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'url',
            'like',
            'title',
            'author',
            'publication_time',
            'cooking_time',
            'servings',
            'description',
            'nutrition',
            'products',
            'images',
            'steps',
        ]
        read_only_fields = ['url', 'publication_time', 'author']