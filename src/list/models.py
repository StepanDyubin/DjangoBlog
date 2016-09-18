from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.core.urlresolvers import reverse


from markdown_deux import markdown


# Create your models here.


class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
		#publish__lte - pozhe ukazanogo




def upload_location(instance, filename):
	return "%s/%s" %(instance.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	title = models.CharField(max_length=100)
	draft = models.BooleanField(default = False)
	publish = models.DateTimeField(auto_now=False, auto_now_add=False)
	content = models.TextField()
	slug = models.SlugField(unique=True)
	#image = models.FileField(null=True, blank=True)
	image = models.ImageField(upload_to=upload_location,
							null=True,
							blank=True,
							height_field="height_field",
							width_field="width_field"
							)
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	

	objects = PostManager()
	# post_like = models.IntegerField(default=0)
	


	def get_absolute_url(self):
		return reverse("List:post_detail", args=[str(self.slug)])

	def get_markdown(self):
		content = self.content
		markedContent = markdown(content)
		return mark_safe(markedContent)


	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title, True)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)




pre_save.connect(pre_save_post_receiver, sender=Post)

