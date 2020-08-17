from rest_framework import serializers
from news.models import News, Country, Tags, Source

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = (
            'id',
            'name',
            'image',
            'country_cod',
            )

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'id',
            'name',
            )

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = (
            'id',
            'name',
            )

class NewsSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    tags =  TagsSerializer(many=True)
    source =  SourceSerializer(read_only=True)
    class Meta:
        model = News
        fields = (
            'id',
            'url',
            'title',
            'headline',
            'explanation',  
            'publication_date',
            'tags',
            'image',
            'source',
            'editor',
            'country',
            )