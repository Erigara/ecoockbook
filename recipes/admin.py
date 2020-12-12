from django.contrib import admin, auth
from recipes.models import Recipe, Nutrition, Product, Step, RecipeImage, Chef
from django.utils.translation import gettext_lazy as _


class NutritionInline(admin.TabularInline):
    model = Nutrition


class ProductInline(admin.TabularInline):
    model = Product


class RecipeImageInline(admin.TabularInline):
    model = RecipeImage


class StepInline(admin.StackedInline):
    model = Step


@admin.register(Recipe)
class Recipe(admin.ModelAdmin):
    readonly_fields = ('id', 'publication_time')
    fieldsets = (
        (_('General info'), {'fields': ('title', 'author', 'publication_time')}),
        (_('Abstract'), {'fields': ('cooking_time', 'servings')}),
        (_('Payload'), {
            'fields': ('description', ),
        }),
    )
    inlines = [
        NutritionInline,
        ProductInline,
        RecipeImageInline,
        StepInline,
    ]
    list_display = ('title', 'author', 'publication_time')
    search_fields = ('title', 'author', 'publication_time')


class ChefInline(admin.StackedInline):
    model = Chef
    can_delete = False


# хак, чтобы получить текущую модель UserAdmin
UserAdmin = admin.site._registry[auth.get_user_model()].__class__
class InlinedChefUserAdmin(UserAdmin):
    inlines = (*UserAdmin.inlines, ChefInline)


# Re-register UserAdmin
admin.site.unregister(auth.get_user_model())
admin.site.register(auth.get_user_model(), InlinedChefUserAdmin)
