from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe, Chef
from recipes.serializers import RecipeSerializer, ChefSerializer, LikeSerializer


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


class LikeView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    queryset = Recipe.objects.all()

    @property
    def chef(self) -> Chef:
        return self.request.user.chef

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # костыль чтобы не плодить код
        self._remove = True
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        remove = getattr(self, '_remove', False)
        serializer.save(chef=self.chef, remove=remove)

    def get_serializer_context(self):
        context = super(LikeView, self).get_serializer_context()
        return context | {'chef': self.chef}


class LikedRecipesListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def get_queryset(self):
        chef = self.request.user.chef
        return chef.likes.all()


class BookmarkedRecipesListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def get_queryset(self):
        chef = self.request.user.chef
        return chef.bookmarks.all()
