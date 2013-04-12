from django.contrib import admin
from transcriptome.models.transcript import Transcript
from transcriptome.models.homology import Homology

admin.site.register(Transcript)
admin.site.register(Homology)
