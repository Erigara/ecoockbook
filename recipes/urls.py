from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipes.views import ChefViewSet, LikeListView, \
    BookmarkListView, RecipeListCreateView, RecipeView, LikeView

router = DefaultRouter()
router.register(r'', ChefViewSet, basename='chef')

urlpatterns = [
    path('', RecipeListCreateView.as_view(), name='recipe'),
    path('<int:pk>', RecipeView.as_view(), name='recipe-detail'),
    path('<int:pk>/likes', LikeView.as_view()),
    # path('<int:pk>/bookmarks'),
    path('likes', LikeListView.as_view()),
    path('bookmarks', BookmarkListView.as_view()),
    path('chefs/', include(router.urls)),
]
