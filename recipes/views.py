from rest_framework import generics, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Recipe, Chef, Like, Category
from recipes.serializers import RecipeSerializer, ChefSerializer, LikeSerializer, CategorySerializer


class ChefMixin:
    @property
    def chef(self) -> Chef:
        return getattr(self.request.user, 'chef', None)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context | {'chef': self.chef}


class ChefViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChefSerializer
    queryset = Chef.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(detail=True)
    def recipes(self, request, pk=None):
        queryset = self.get_object().recipes
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RecipeSerializer(page, many=True, context=self.get_serializer_context())
            return self.get_paginated_response(serializer.data)

        serializer = RecipeSerializer(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)



class RecipeViewSet(ChefMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    @action(detail=False)
    def favorites(self, request):
        queryset = self.chef.likes.all()
        return self._list_queryset(queryset)

    def _list_queryset(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class RecipeListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class RecipeView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class LikeView(ChefMixin,
               mixins.RetrieveModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    lookup_url_kwarg = 'recipe'


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Like.objects.filter(chef=self.chef)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        recipe = self.recipe
        try:
            obj = queryset.get(recipe=recipe)
        except Like.DoesNotExist:
            obj = Like(
                chef=self.chef,
                recipe=recipe,
            )

        self.check_object_permissions(self.request, obj)
        return obj

    @property
    def recipe(self) -> Recipe:
        return get_object_or_404(Recipe, pk=self.kwargs[self.lookup_url_kwarg])

    def perform_create(self, serializer):
        serializer.save(recipe=self.recipe, chef=self.chef)

    def perform_destroy(self, instance):
        if not instance._state.adding:
            instance.delete()


class LikedRecipeListView(ChefMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return self.chef.likes.all()


class InCategoryRecipeListView(ChefMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Recipe.objects.filter(category__pk=self.kwargs['category'])

