from django.db import models
from transcriptome.models.refseq import Refseq


class CommonMutation(models.Model):
    hit_name = models.ForeignKey(Refseq, to_field='accession')
    formothion = models.BooleanField()
    fenthion = models.BooleanField()
    methomyl = models.BooleanField()
    # intersection = models.CharField(max_length=15)
