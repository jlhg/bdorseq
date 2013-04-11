from django.conf.urls import patterns, url
from transcriptome import views

urlpatterns = patterns('',
                       url(r'^$', views.transcript.index, name='index'),
                       url(r'^login/', views.transcript.signin, name='signin'),
                       url(r'^search/?P<transcript_acc>\w+', views.transcript.search, name='search')
                       )
