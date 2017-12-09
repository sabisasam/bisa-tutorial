from django.conf.urls import url

from . import views


app_name = 'webhook'
urlpatterns = [
    # ex: /api/hello/
    url(r'^api/hello/$', views.hello, name='hello'),
]
