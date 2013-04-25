from django.db import models


class Refseq(models.Model):
    refacc = models.CharField(max_length=20)
    refseq = models.TextField()
    refdes = models.TextField()

    class Meta:
        app_label = 'transcriptome'
