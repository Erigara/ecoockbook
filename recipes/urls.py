from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import ChefViewSet, LikeListView, RecipeListCreateView, RecipeView, LikeView

router = DefaultRouter()
router.register(r'', ChefViewSet, basename='chef')

urlpatterns = [
    path('', RecipeListCreateView.as_view(), name='recipe'),
    path('<int:pk>', RecipeView.as_view(), name='recipe-detail'),
    path('<int:recipe>/like', LikeView.as_view(), name='like-detail'),
    path('likes', LikeListView.as_view(), name='like'),
    path('chefs/', include(router.urls)),
]