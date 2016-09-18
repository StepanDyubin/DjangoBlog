from django.contrib import admin

# Register your models here.
from .models import Post 


class PostModelAdmin(admin.ModelAdmin):
	class Meta:
		model = Post
	list_display = ['title','updated','timestamp']
	#list_editable = ['title']
	list_filter = ['updated','timestamp']
	search_fields = ['title']

admin.site.register(Post, PostModelAdmin)