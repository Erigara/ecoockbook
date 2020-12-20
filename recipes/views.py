from rest_framework import generics, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Recipe, Chef, Like, Category, RecipeImage, Step, Product
from recipes.serializers import RecipeSerializer, ChefSerializer, LikeSerializer, CategorySerializer, \
    RecipeImageSerializer, StepSerializer, ProductSerializer, MoveStepSerializer


class ChefMixin:
    @property
    def chef(self) -> Chef:
        return getattr(self.request.user, 'chef', None)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context | {'chef': self.chef}


class RecipeMixin:
    @property
    def recipe(self):
        recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe'])
        return recipe

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context | {'recipe': self.recipe}


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


class RecipeComponentViewSet(RecipeMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    model = None

    def get_queryset(self):
        if self.model is None:
            raise NotImplemented('Subclass of RecipeViewSet must override model')
        return self.model.objects.filter(recipe=self.recipe)

    def perform_create(self, serializer):
        serializer.save(recipe=self.recipe)


class RecipeImageViewSet(RecipeComponentViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = RecipeImageSerializer
    model = RecipeImage


class StepViewSet(RecipeComponentViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = StepSerializer
    model = Step

    def perform_destroy(self, instance):
        Step.objects.move(instance)
        instance.delete()


class MoveStepView(RecipeMixin, generics.GenericAPIView):
    serializer_class = MoveStepSerializer

    def get_queryset(self):
        return Step.objects.filter(recipe=self.recipe)

    def put(self, request, *args, **kwargs):
        """
        Move a single Step to a new position
        """
        obj = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_order = serializer.validated_data.get('order')

        Step.objects.move(obj, new_order)

        return Response({'success': True, 'order': new_order})


class ProductViewSet(RecipeComponentViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductSerializer
    model = Product


class RecipeViewSet(ChefMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    @action(detail=False, methods=['post'])
    def template(self, requst):
        instance = Recipe.template(author=self.chef)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False)
    def favorites(self, request):
        queryset = self.chef.likes.all()
        return self._list_queryset(queryset)

    @action(detail=False)
    def own(self, request):
        queryset = Recipe.objects.filter(author=self.chef)
        return self._list_queryset(queryset)

    def _list_queryset(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.chef)


class LikeView(ChefMixin,
               RecipeMixin,
               mixins.RetrieveModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

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

    def perform_create(self, serializer):
        serializer.save(recipe=self.recipe, chef=self.chef)

    def perform_destroy(self, instance):
        if not instance._state.adding:
            instance.delete()
