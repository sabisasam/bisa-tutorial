from django.conf.urls import url

from . import views


app_name = 'fortune'
urlpatterns = [
    # ex: /fortune/
    url(r'^$', views.index, name='index'),
    # ex: /fortune/starwars/
    url(r'^(?P<category>[\w\- ]+)/$', views.fortune_category, name='fortune-category'),
    # ex: /fortune/normal/
    url(r'^normal/$', views.fortune_normal, name='fortune-normal'),
    # ex: /fortune/rabbitmq/
    url(r'^rabbitmq/$', views.fortune_rabbitmq, name='fortune-rabbitmq'),
    # ex: /fortune/websocket/
    url(r'^websocket/$', views.fortune_websocket, name='fortune-websocket'),
]
