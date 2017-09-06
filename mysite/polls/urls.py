from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # ex: /polls/random1/
    url(r'^random1/$', views.Random1View.as_view(), name='random-queryset'),
    # ex: /polls/random/
    url(r'^random/$', views.RandomView.as_view(), name='random-number'),
    # ex: /polls/questions/
    url(r'^questions/$', views.questions, name='questions'),
    # ex: /polls/questions/index/
    url(r'^questions/index/$', views.questionsIndex, name='questions-index'),
    # ex: /polls/questions/?page=5/archived/
    url(r'^questions/(?P<page_num>[0-9]+)/archived/$', views.questionsArchive, name='questions-archive'),
]
