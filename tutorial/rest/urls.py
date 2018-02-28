from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'rest'
urlpatterns = [
    url(r'^$', views.SnippetList.as_view(), name='snippet-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view(), name='snippet-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
