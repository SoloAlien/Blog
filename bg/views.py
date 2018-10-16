from django.shortcuts import render, HttpResponse
from bg.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def article_detail(req, year, month, day, slug):
    article = Article.manager.filter(publish__year=year, publish__month=month, publish__day=day, slug=slug)[0]
    url = reverse('share_article', args=[article.id])
    comments = Comment.objects.filter(article=article)
    comment_list = Article.get_comment_list(article, comments=comments)
    print(comment_list.__len__())
    for i in comment_list:
        print('------------->',i)
        print('------------->',i.comment_children)
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


from bg.forms import share_form
from django.core.mail import send_mail


def share_article(req, article_id):
    article = None
    data = None
    article = Article.manager.filter(id=article_id)[0]
    if req.method == 'POST':
        form = share_form(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = "{}({})推荐你阅读文章{}".format(data['title'], data['send'], article.title)
            msg = data['comment']
            send_mail(subject=subject, message=msg, from_email='xxx@163.com', recipient_list={data['to']},
                      fail_silently=True)
            return HttpResponse("ok")
    else:
        form = share_form()
    return render(req, 'share_article.html', locals())
