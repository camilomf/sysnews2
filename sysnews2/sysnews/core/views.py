from django.shortcuts import render
from django.apps import apps
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from news.models import News, Country, Tags
from news.forms import NewsForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q
from django.contrib.auth.models import Group, User
from django.http import HttpResponse, JsonResponse
import json
from django.core import serializers
from news.views import tagsSerializer
import datetime

# Create your views here.
class HomePageView(ListView):
    queryset = News.objects.all()
    template_name = "core/home.html"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all().order_by('name')
        context['tags_list'] = Tags.objects.all()
        context['users'] = User.objects.filter(groups=2)
        list_news = News.objects.all()
        paginator = Paginator(list_news, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)

        # context = context_permanent(None)
        context['list_news'] = file_exams
        return context

def is_valid_queryparam(param):
    return param != '' and param is not None and len(param) > 0

def formatDate(date):
    nd = date.split('/')
    mm = nd [0]
    dd = nd [1]
    yy = nd [2]
    return str(yy+"-"+mm+"-"+dd)

def searchFilter(request):
    qs = News.objects.all()
    title_contains_query = request.GET.get('title_contains')
    daterange_query = request.GET.get('daterange')
    country_query = request.GET.getlist('countries')
    tags_query = request.GET.getlist('tags')

    if is_valid_queryparam(tags_query):
        print ("tags")
        for q in tags_query:
            qs = qs.filter(tags__id=q)
            print (qs)

    if is_valid_queryparam(title_contains_query):
        print ("title")
        qs = qs.filter(title__icontains=title_contains_query)

    if is_valid_queryparam(daterange_query):
        print (daterange_query)
        daterange_query = daterange_query.split(' - ')
        daterange_query[0] = formatDate(daterange_query[0])
        daterange_query[1] = formatDate(daterange_query[1])
        qs = qs.filter(publication_date__range=[daterange_query[0],daterange_query[1]])

    if is_valid_queryparam(country_query):
        print ("country")
        print (country_query)
        qs = qs.filter(country__in=country_query)

    print (qs)

    context = {
        'list_news' : qs
    }
    return render(request,"core/home.html",context)

def searchNews(request):
    qs = News.objects.all()
    daterange_query = request.GET.get('daterange')
    if is_valid_queryparam(daterange_query):
        daterange_query = daterange_query.split(' - ')
        qs = qs.filter(publication_date__range=[daterange_query[0],daterange_query[1]]).order_by('country')
        qs = [ newsSerializer(news) for news in qs ]
        return HttpResponse(json.dumps(qs),content_type='application/json')

def newsList(request):
    list_news = News.objects.all()
    list_news = [ newsSerializer(news) for news in list_news ]
    return HttpResponse(json.dumps(list_news),content_type='application/json')

def newsSerializer(news):
    return {
        'id':news.id,
        'title':news.title,
        'headline':news.headline,
        'tags': news.tags.name,
        'image':"http://127.0.0.1:8000"+news.image.url,
        'explanation': news.explanation,
        'date': str(news.publication_date),
        'country':news.country.name
        }

@login_required
def countryList(request):
    countries = Country.objects.all()
    countries = [ countrySerializer(country) for country in countries ]
    return HttpResponse(json.dumps(countries),content_type='application/json')

def countrySerializer(country):
    return {'id':country.id,'name':country.name}

@login_required
def tagByCountry(request):
    if request.method == 'GET':
        country_ids = request.GET.getlist('country[]')
        qs = Tags.objects.all()
        nid = News.objects.filter(country__id__in=country_ids).values_list('id', flat=True)
        tig = Tags.objects.filter(news__id__in=[nid]).values_list('id', flat=True)
        tags = Tags.objects.filter(id__in=[tig])
        tags = [ tagsSerializer(tag) for tag in tags ]
        return HttpResponse(json.dumps(tags),content_type='application/json')

@login_required
def countryByTag(request):
    if request.method == 'GET':
        tag_ids = request.GET.getlist('tag[]')
        qs = Country.objects.all()
        nid = News.objects.filter(tags__id__in=tag_ids).values_list('id', flat=True)
        tig = News.objects.filter(id__in=[nid]).values_list('country_id').distinct()
        countries = Country.objects.filter(id__in=[tig])
        countries = [ countrySerializer(country) for country in countries ]
        return HttpResponse(json.dumps(countries),content_type='application/json')

        



"""
SELECT news_tags.name from news_tags WHERE news_tags.id 
IN ( SELECT news_news_tags.tags_id from news_news_tags where news_news_tags.news_id 
in (SELECT news_news.id FROM `news_news` WHERE news_news.country_id = 1) )
"""

# @login_required
# def searchByCountry(request, id):
#     # id=Country.objects.filter(name=q)
#     news = News.objects.filter(country=id)
#     # context = {}
#     context = context_permanent(news)
#     # context['news_list'] = news
#     # context['countries'] = Country.objects.all()
#     # context['editors'] = User.objects.filter(groups=2)
#     return render(request, 'core/home.html', context)

    
# @login_required
# def searchByUser(request, **kwargs):
#     q = request.POST.get('search_by_user')
#     news = News.objects.filter(editor=q).order_by('-created')
#     context = context_permanent(news)
#     # context = {}
#     # context['news_list'] = news
#     # context['countries'] = Country.objects.all()
#     return render(request, 'core/home.html', context)
