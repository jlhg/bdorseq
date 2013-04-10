from django.contrib import admin
from transcriptome.models import Transcript, Refseq

admin.site.register(Transcript)
admin.site.register(Refseq)
