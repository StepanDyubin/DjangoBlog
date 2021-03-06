from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from list.models import Post


class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
	#post = models.ForeignKey(Post)

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	comment_content = models.TextField(max_length=3000)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.user.username)

	def __str__(self):
		return str(self.user.username)