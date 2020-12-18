from rest_framework import generics, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe, Chef, Like
from recipes.serializers import RecipeSerializer, ChefSerializer, LikeSerializer


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


class LikeListView(ChefMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(chef=self.chef)
