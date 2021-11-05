from django.urls import path

from . import views


app_name = 'fortune'
urlpatterns = [
    # ex: /fortune/
    path('', views.index, name='index'),
    # ex: /fortune/category/starwars/
    path('category/<str:category>/', views.fortune_category, name='fortune-category'),
    # ex: /fortune/normal/
    path('normal/', views.fortune_normal, name='fortune-normal'),
    # ex: /fortune/rabbitmq/
    path('rabbitmq/', views.fortune_rabbitmq, name='fortune-rabbitmq'),
    # ex: /fortune/websocket/
    path('websocket/', views.fortune_websocket, name='fortune-websocket'),
]
