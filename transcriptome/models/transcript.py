from django.db import models


class Transcript(models.Model):
    seqname = models.CharField(max_length=50, unique=True)
    seq = models.TextField()
    line = models.CharField(max_length=6)
    species = models.CharField(max_length=40)
    owner = models.CharField(max_length=15)
    platform = models.CharField(max_length=15)

    class Meta:
        app_label = 'transcriptome'
