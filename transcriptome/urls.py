from django.conf.urls import patterns, url
from transcriptome.views import accounts, transcript, document, archive
from transcriptome.views import seqvar

urlpatterns = patterns('',
                       url(r'^$', transcript.index, name='index'),
                       url(r'^login/', accounts.signin, name='signin'),
                       url(r'^logout/', accounts.signout, name='signout'),
                       url(r'^search/', transcript.search, name='search'),
                       url(r'^export/', transcript.export, name='export'),
                       url(r'^help/', document.help, name='help'),
                       url(r'^details/(?P<seqname>[A-Z0-9.]+)/', transcript.details, name='details'),
                       url(r'^archive/', archive.search, name='archive'),
                       url(r'^seqvar/search/', seqvar.search, name='svsearch'),
                       url(r'^seqvar/details/(?P<commonset>[a-z_]+)/(?P<refacc>[A-Z0-9._]+)/', seqvar.details, name='svdetail'),
                       url(r'^changelog/', document.changelog, name='changelog'),
                       )
