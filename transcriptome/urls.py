from django.conf.urls import patterns, url
from transcriptome.views import transcript, document

urlpatterns = patterns('',
                       url(r'^$', transcript.index, name='index'),
                       url(r'^login/', transcript.signin, name='signin'),
                       url(r'^logout/', transcript.signout, name='signout'),
                       url(r'^search/', transcript.search, name='search'),
                       url(r'^export/', transcript.export, name='export'),
                       url(r'^help/', document.help, name='help'),
                       url(r'^details/(?P<seqname>[A-Z0-9.]+)/', transcript.details, name='details')
                       )
