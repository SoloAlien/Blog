from django.contrib import admin
from bg.models import *


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'status', 'publish']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
