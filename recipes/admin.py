from django.contrib import admin, auth
from recipes.models import Recipe, Nutrition, Product, Step, RecipeImage, Chef, Like, Category, CookingTime, Comment
from django.utils.translation import gettext_lazy as _


class NutritionInline(admin.TabularInline):
    model = Nutrition


class CookingTimeInline(admin.TabularInline):
    model = CookingTime


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 0


class StepInline(admin.StackedInline):
    model = Step
    extra = 0

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'publication_time')
    fieldsets = (
        (_('general info'), {'fields': ('title', 'author', 'publication_time', 'category')}),
        (_('abstract'), {'fields': ('servings', )}),
        (_('Payload'), {
            'fields': ('description', ),
        }),
    )
    inlines = [
        NutritionInline,
        ProductInline,
        RecipeImageInline,
        StepInline,
        CommentInline,
    ]
    list_display = ('id', 'title', 'author', 'publication_time')
    search_fields = ('id', 'title', 'author', 'publication_time')


class LikeInline(admin.TabularInline):
    model = Like
    extra = 0


class OwnRecipesInline(admin.StackedInline):
    model = Recipe
    extra = 0
    verbose_name = _('own recipe')
    verbose_name_plural = _('own recipes')


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user')
    inlines = [OwnRecipesInline, LikeInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
