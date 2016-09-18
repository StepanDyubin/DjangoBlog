from django.conf.urls import url


from . import views

app_name = 'list'

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^create/$', views.post_create, name='post_create'),
	url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='post_detail'),  #from rege to views
	url(r'^(?P<slug>[\w-]+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='post_delete'),
]
