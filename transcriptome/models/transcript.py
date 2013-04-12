from django.db import models
from transcriptome.models.homology import Homology


class Transcript(models.Model):
    accession = models.CharField(max_length=10)
    seq_name = models.CharField(max_length=50)
    seq = models.TextField()
    insecticide = models.CharField(max_length=15)
    line = models.CharField(max_length=15)
    species = models.CharField(max_length=40)
    owner = models.CharField(max_length=15)
    platform = models.CharField(max_length=15)
    homology = models.ForeignKey(Homology)

    class Meta:
        app_label = 'transcriptome'
