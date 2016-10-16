from django.conf.urls import patterns, url

from taskmanager import views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^create-tags/$', views.create_tags, name='create_tags'),
    url(r'^get-tasks/$', views.get_tasks, name='get_tasks'),
    url(r'^get-tags/$', views.get_tags, name='get_tags'),
    url(r'^remove-task/$', views.remove_task, name='remove_task'),
    url(r'^create-or-update-task/$', views.create_or_update_task, name='create_or_update_task'),
    url(r'^get-task-details/(?P<id>\d+)/$', views.get_task, name='get_task'),
    url(r'^get-tag-details/(?P<id>\d+)/$', views.get_tag, name='get_tag'),
    url(r'^update-or-delete-tag/$', views.update_or_delete_tag, name='update_or_delete_tag'),
    url(r'^login/$',auth_views.login, name = "login_view")
) 