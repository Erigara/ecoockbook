from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter

from recipes.views import ChefViewSet, LikeView, CategoryViewSet, \
    RecipeViewSet, RecipeImageViewSet, StepViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'chefs', ChefViewSet, basename='chef')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'recipes/(?P<recipe>[^/.]+)/images', RecipeImageViewSet, basename='recipe-image')
router.register(r'recipes/(?P<recipe>[^/.]+)/steps', StepViewSet, basename='recipe-step')
router.register(r'recipes/(?P<recipe>[^/.]+)/products', ProductViewSet, basename='recipe-product')


urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe>/likes', LikeView.as_view(), name='recipe-like'),
    # path('likes/recipes', LikedRecipeListView.as_view(), name='recipe-favorites'),
    # path('categories/<int:category>/recipes', InCategoryRecipeListView.as_view(), name='recipe-in-category'),

]
