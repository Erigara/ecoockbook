from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter

from recipes.views import ChefViewSet, LikedRecipeListView, RecipeListCreateView, RecipeView, LikeView, CategoryViewSet, \
    InCategoryRecipeListView, RecipeViewSet

router = DefaultRouter()
router.register(r'chefs', ChefViewSet, basename='chef')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'recipes', RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe>/likes', LikeView.as_view(), name='likes'),
    # path('likes/recipes', LikedRecipeListView.as_view(), name='recipe-favorites'),
    # path('categories/<int:category>/recipes', InCategoryRecipeListView.as_view(), name='recipe-in-category'),

]
