from django.conf.urls import patterns, url
from transcriptome.views import accounts, transcript, document, archive

urlpatterns = patterns('',
                       url(r'^$', transcript.index, name='index'),
                       url(r'^login/', accounts.signin, name='signin'),
                       url(r'^logout/', accounts.signout, name='signout'),
                       url(r'^search/', transcript.search, name='search'),
                       url(r'^export/', transcript.export, name='export'),
                       url(r'^help/', document.help, name='help'),
                       url(r'^details/(?P<seqname>[A-Z0-9.]+)/', transcript.details, name='details'),
                       url(r'^archive/', archive.search, name='archive')
                       )
