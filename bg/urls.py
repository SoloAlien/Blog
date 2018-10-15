from django.urls import path, re_path
from bg.views import *

urlpatterns = [
    path('article_list/', article_list),
    re_path('article_detail/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<slug>[\w-]+)/', article_detail,
            name='article_detail'),
    path('share_article/<int:article_id>/', share_article, name='share_article'),
]
