from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.routers import DefaultRouter

from recipes.views import ChefViewSet, LikeView, CategoryViewSet, \
    RecipeViewSet, RecipeImageViewSet, StepViewSet, ProductViewSet, MoveStepView, CommentViewSet

router = DefaultRouter()
router.register(r'chefs', ChefViewSet, basename='chef')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'recipes/(?P<recipe>[^/.]+)/images', RecipeImageViewSet, basename='recipe-image')
router.register(r'recipes/(?P<recipe>[^/.]+)/steps', StepViewSet, basename='recipe-step')
router.register(r'recipes/(?P<recipe>[^/.]+)/products', ProductViewSet, basename='recipe-product')
router.register(r'recipes/(?P<recipe>[^/.]+)/comments', CommentViewSet, basename='recipe-comment')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe>/likes', LikeView.as_view(), name='recipe-like'),
    path('recipes/<int:recipe>/steps/<int:pk>/move', MoveStepView.as_view(), name='recipe-step-detail-move'),
]
