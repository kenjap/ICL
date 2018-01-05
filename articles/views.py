from urllib import quote_plus

from django.contrib import messages
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ArticleForm
from .models import Article


def article_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404

	if not request.user.is_authenticated():
		raise Http404

	form = ArticleForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Successfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	else:
		messages.error(request, "Not successfully created")
	context = {
		"form": form,
	}
	return render(request, "article_form.html", context)

def article_detail(request, slug=None):
	instance = get_object_or_404(Article, slug=slug)
	if instance.draft or instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context = {
		"title": instance.title,
		"instance": instance,
		"share_string": share_string,
	}
	return render(request, "article_detail.html", context)

def article_list(request):
	today = timezone.now().date()
	queryset_list = Article.objects.active()
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Article.objects.all()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(user__first_name__icontains=query)|
			Q(user__last_name__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list  , 10) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		"object_list": queryset,
		"title": "Intercultural Living - blog",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "article_list.html", context)

def article_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Article, slug=slug)
	
	form = ArticleForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> saved", extra_tags = 'html_safe')
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title": instance.title,
		"instance": instance,
		"form": form,
	}
	#messe
	return render(request, "article_form.html", context)


def article_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Article, slug=slug)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("articles:list")
