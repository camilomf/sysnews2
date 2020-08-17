from news.models import News, Country, Tags, Source
from .serializers import NewsSerializer, SourceSerializer, TagsSerializer, CountrySerializer
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from django_filters import rest_framework as filters

# Create your views here.
class NewsFilter(FilterSet):
    title = filters.CharFilter('title')
    min_date = filters.CharFilter(method="filter_by_min")
    max_date = filters.CharFilter(method="filter_by_max")

    class Meta:
        model = News
        fields = (
            'title',
            'publication_date',
            )
    
    def filter_by_min(self,queryset,name,value):
        queryset = queryset.filter(publication_date__gte=value)
        return queryset

    def filter_by_max(self,queryset,name,value):
        queryset = queryset.filter(publication_date__lte=value)
        return queryset


class NewsView(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (DjangoFilterBackend,OrderingFilter)
    # search_fields = ['publication_date']
    # filter_fields = ('publication_date','title')
    filter_class = NewsFilter








