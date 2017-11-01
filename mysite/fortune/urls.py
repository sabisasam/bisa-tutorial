from django.conf.urls import url

from . import views


app_name = 'fortune'
urlpatterns = [
    # ex: /fortune/
    url(r'^$', views.index, name='index'),
    # ex: /fortune/normal/
    url(r'^normal/$', views.fortuneNormal, name='fortune-normal'),
    # ex: /fortune/websocket/
    url(r'^websocket/$', views.fortuneWebsocket, name='fortune-websocket'),
]
