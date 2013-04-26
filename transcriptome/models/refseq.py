from django.db import models


class Refseq(models.Model):
    accession = models.CharField(max_length=20, unique=True)
    seq = models.TextField()
    description = models.TextField()

    class Meta:
        app_label = 'transcriptome'
