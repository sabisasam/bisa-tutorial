from django.conf.urls import url

from . import views


app_name = 'fortune'
urlpatterns = [
    # ex: /fortune/
    url(r'^$', views.index, name='index'),
]
