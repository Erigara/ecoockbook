from django.template import loader
from elasticsearch_dsl import Q
from rest_framework import filters
from recipes.documents import RecipeDocument


class RecipeFilterBackend(filters.BaseFilterBackend):
    """
    Поиск по полям запроса:
        * поиск по авторам
        * категориям
        * тексту в рецепте и его шагах
    """
    template = 'rest_framework/filters/search.html'

    def filter_queryset(self, request, queryset, view):
        search = request.query_params.get('search', None)
        if search:
            query_in_reipe = Q(
                "multi_match",
                query=search,
                fields=[
                    'title',
                    'author',
                    'category.name',
                    'description',
                ])
            query_in_steps = Q(
                "nested",
                path='steps',
                query=Q("match", steps__description=search)
            )
            query_in_products = Q(
                "nested",
                path='products',
                query=Q("match", products__name=search)
            )
            query = RecipeDocument.search().query(query_in_reipe | query_in_steps | query_in_products)
            queryset = query.to_queryset()

        return queryset

    def to_html(self, request, queryset, view):
        search = request.query_params.get('search', '')
        context = {
            'param': 'search',
            'term': search
        }
        template = loader.get_template(self.template)
        return template.render(context)
