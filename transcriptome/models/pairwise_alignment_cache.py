from django.db import models


class PairwiseAlignmentCache(models.Model):
    tool = models.CharField(max_length=15)
    query_name = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=50)
    alignment_dna = models.TextField(null=True)
    alignment_dna_html = models.TextField(null=True)
    alignment_protein = models.TextField(null=True)
    alignment_protein_html = models.TextField(null=True)

    class Meta:
        app_label = 'transcriptome'
