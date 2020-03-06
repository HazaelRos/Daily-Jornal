"""Defines URL patterns for journal."""
from django.urls import path, re_path, include

from . import views

app_name = "journal"
urlpatterns = [
    #home page.
     re_path(r'^$', views.index, name='index'),
     #topics page: shows all.
     re_path(r'^topics/$', views.topics, name='topics'),
     #single topic.
     re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
     #new topic
     re_path(r'^new_topic/$', views.new_topic, name='new_topic'),
     #new entry
     re_path(
     r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
     #edit entry
     re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry,
     name='edit_entry'),
]
