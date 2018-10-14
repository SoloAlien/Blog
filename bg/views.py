from django.shortcuts import render, HttpResponse
from bg.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def article_detail(req, year, month, day, slug):
    article = Article.manager.filter(publish__year=year, publish__month=month, publish__day=day, slug=slug)[0]
    return render(req, 'article_detail.html', locals())


def article_list(req):
    articles = Article.manager.all()
    paginator = Paginator(articles, 3)
    nowPage = req.GET.get("nowPage")
    if nowPage:
        try:
            page = paginator.page(nowPage)
        except EmptyPage:
            page = paginator.page(1)
        except PageNotAnInteger:
            page = paginator.page(1)
    else:
        page = paginator.page(1)
    return render(req, 'list.html', locals())
