from urllib import quote_plus
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect	
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

#import forms
from .forms import PostForm

# import models
from comments.models import Comment
from .models import Post

# Create your views here.

def post_list(request):
	queryset_list = Post.objects.all().order_by('-updated')
	if not request.user.is_staff or not request.user.is_superuser:
		queryset_list = Post.objects.active().order_by('-updated')

	today = timezone.now()

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query) 
				).distinct()
	paginator = Paginator(queryset_list, 10 ) #Show 5 contacts per page
	page_request_var='page'#url name 'page'=1,2,3,4...
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
		"object_list": queryset,#object_list v html
		"today": today,
		"page_request_var": page_request_var #v url num page

	}
	return render(request, "post_list.html", context)


def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Successfuly created", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())	
	context = {
		'form': form
	}
	return render(request, "post_form.html", context)

def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if  instance.draft or instance.publish > timezone.now():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	# share_content = quote_plus(instance.content)
	content_type = ContentType.objects.get_for_model(Post)
	obj_id = instance.id
	comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)

	context = {
		'instance': instance,
		'comments': comments,
		# 'share_content': share_content
	}
	return render(request, "post_detail.html", context)

def post_edit(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Item</a> edited", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		'instance': instance,
		'form': form
	}
	return render(request, "post_form.html", context)
	

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfuly deleted", extra_tags="html_safe")
	context = {
	}
	return redirect("List:post_list")
