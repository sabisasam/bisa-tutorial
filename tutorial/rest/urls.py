from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'rest'
urlpatterns = [
    url(r'^$', views.snippet_list, name='snippet-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.snippet_detail, name='snippet-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
