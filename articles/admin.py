from django.contrib import admin
from .models import Article

# Register your models here.

class ArticleModelAdmin(admin.ModelAdmin):
	list_display = ["__unicode__", "update", "timestamp"]
	list_filter = [ "update", "timestamp"]
	class Meta:
		model = Article



admin.site.register(Article, ArticleModelAdmin)