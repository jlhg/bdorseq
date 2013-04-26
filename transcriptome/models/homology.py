from django.db import models
from transcriptome.models.transcript import Transcript
from transcriptome.models.refseq import Refseq


class Homology(models.Model):
    tool = models.CharField(max_length=15)
    query_name = models.ForeignKey(Transcript, to_field='seqname', unique=True)
    hit_name = models.ForeignKey(Refseq, to_field='accession')
    query_length = models.PositiveIntegerField(max_length=8)
    query_hsp_start = models.PositiveIntegerField(max_length=8)
    query_hsp_end = models.PositiveIntegerField(max_length=8)
    query_strand = models.CharField(max_length=2)
    query_frame = models.IntegerField(max_length=2)
    hit_length = models.PositiveIntegerField(max_length=8)
    hit_hsp_start = models.PositiveIntegerField(max_length=8)
    hit_hsp_end = models.PositiveIntegerField(max_length=8)
    hit_strand = models.CharField(max_length=2)
    hit_frame = models.IntegerField(max_length=2)
    hsp_score = models.IntegerField(max_length=4)
    hsp_bits = models.FloatField(max_length=10)
    hsp_evalue = models.FloatField(max_length=10)
    hsp_length = models.PositiveIntegerField(max_length=8)
    hsp_gaps = models.PositiveIntegerField(max_length=5)
    hsp_identities = models.PositiveIntegerField(max_length=8)
    hsp_identity_percent = models.FloatField(max_length=6)
    hsp_positives = models.PositiveIntegerField(max_length=8)
    hsp_positive_percent = models.FloatField(max_length=6)
    query_coverage = models.FloatField(max_length=6)
    hit_coverage = models.FloatField(max_length=6)
    hit_description = models.TextField()

    class Meta:
        app_label = 'transcriptome'
