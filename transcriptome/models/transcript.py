from django.db import models


class Transcript(models.Model):
    accession = models.CharField(max_length=10, unique=True)
    seqname = models.CharField(max_length=50, unique=True)
    seq = models.TextField()
    line = models.CharField(max_length=15)
    species = models.CharField(max_length=40)
    owner = models.CharField(max_length=15)
    platform = models.CharField(max_length=15)

    class Meta:
        app_label = 'transcriptome'
