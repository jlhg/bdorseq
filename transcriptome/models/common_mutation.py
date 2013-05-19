from django.db import models
from transcriptome.models.refseq import Refseq


class CommonMutation(models.Model):
    hit_name = models.ForeignKey(Refseq, to_field='accession')
    formothion = models.BooleanField()
    fenthion = models.BooleanField()
    methomyl = models.BooleanField()
    for_fen = models.BooleanField()
    for_met = models.BooleanField()
    fen_met = models.BooleanField()
    for_fen_met = models.BooleanField()
    for_profile = models.CharField(max_length=200)
    fen_profile = models.CharField(max_length=200)
    met_profile = models.CharField(max_length=200)
    for_fen_profile = models.CharField(max_length=200)
    for_met_profile = models.CharField(max_length=200)
    fen_met_profile = models.CharField(max_length=200)
    for_fen_met_profile = models.CharField(max_length=200)

    class Meta:
        app_label = 'transcriptome'
