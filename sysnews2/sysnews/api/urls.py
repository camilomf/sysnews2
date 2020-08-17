from django.urls import path, include
from .views import NewsView
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('news',views.NewsView)

urlpatterns = [
    path ('news/', NewsView.as_view())
]
