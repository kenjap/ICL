from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class ArticleManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(ArticleManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)


class Article(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=100)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to = upload_location, null=True, blank=True, 
		width_field = 'width_field',
		height_field = 'height_field')
	width_field = models.IntegerField(default=0)
	height_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)	
	update = models.DateTimeField(auto_now=True, auto_now_add=False, blank=True, null=True)

	objects = ArticleManager()

	def __unicode__(self):
		return self.title	

	def __str__(self):
		return self.title


	def snippet(self):
		return self.content[:50] + '...'

	def get_absolute_url(self):
		return reverse("articles:detail", kwargs={"slug":self.slug})

	class Meta:
		ordering = ["-timestamp", "update"]

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Article.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_article_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_article_receiver, sender=Article)	