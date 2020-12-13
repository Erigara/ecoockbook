from rest_framework import serializers

from recipes.models import Recipe, Nutrition, Step, RecipeImage, Product, Chef


class ChefSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Chef
        fields = ['url', 'user', 'likes', 'bookmarks']
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


# TODO обработка вложенных серилизаторов
class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    likes_number = serializers.IntegerField(read_only=True)
    bookmarks_number = serializers.IntegerField(read_only=True)
    nutrition = NutritionSerializer()
    products = ProductSerializer(many=True)
    images = RecipeImageSerializer(many=True)
    steps = StepSerializer(many=True)

    class Meta:
        model = Recipe
        fields = [
            'url',
            'id',
            'title',
            'author',
            'publication_time',
            'cooking_time',
            'servings',
            'description',
            'likes_number',
            'bookmarks_number',
            'nutrition',
            'products',
            'images',
            'steps',
        ]
        read_only_fields = ['url', 'publication_time', 'author']


# TODO валидация на то, что chef не None
class LikeSerializer(serializers.HyperlinkedModelSerializer):
    likes_number = serializers.IntegerField(read_only=True)
    has_like = serializers.SerializerMethodField()

    def update(self, instance: Recipe, validated_data) -> Recipe:
        chef = self.context.get('chef')
        remove = validated_data.pop('remove', False)
        if remove:
            instance.remove_like(chef)
        else:
            instance.set_like(chef)
        instance.save()
        return instance

    def get_has_like(self, instance: Recipe) -> bool:
        chef = self.context.get('chef')
        return instance.has_like(chef)

    class Meta:
        model = Recipe
        fields = [
            'url',
            'likes_number',
            'has_like'
        ]
