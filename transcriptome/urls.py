from django.conf.urls import patterns, url
from transcriptome.views import transcript

urlpatterns = patterns('',
                       url(r'^$', transcript.index, name='index'),
                       url(r'^login/', transcript.signin, name='signin'),
                       url(r'^search/?P<transcript_acc>\w+', transcript.search, name='search')
                       )
