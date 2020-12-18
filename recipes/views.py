from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipe, Chef
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


class LikeView(ChefMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer
    queryset = Recipe.objects.all()

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

# TODO использовать LikeSerilizer
class LikeListView(ChefMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return self.chef.likes.all()


class BookmarkListView(ChefMixin, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return self.chef.bookmarks.all()
