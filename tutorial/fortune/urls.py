from django.conf.urls import url

from . import views


app_name = 'fortune'
urlpatterns = [
    # ex: /fortune/
    url(r'^$', views.index, name='index'),
    # ex: /fortune/normal/
    url(r'^normal/$', views.fortune_normal, name='fortune-normal'),
    # ex: /fortune/websocket/
    url(r'^websocket/$', views.fortune_websocket, name='fortune-websocket'),
    # ex: /fortune/rabbitmq/
    url(r'^rabbitmq/$', views.fortune_rabbitmq, name='fortune-rabbitmq'),
]
