from django.db import models


class Transcript(models.Model):
    accession = models.CharField(max_length=10)
    seq_name = models.CharField(max_length=50)
    seq = models.TextField()
    insecticide = models.CharField(max_length=15)
    line = models.CharField(max_length=15)
    species = models.CharField(max_length=40)
    owner = models.CharField(max_length=15)
    platform = models.CharField(max_length=15)
    # homo_refseq_acc = models.CharField(max_length=10)
    # homo_refseq_des = models.TextField()


class BlastxBest(models.Model):
    tool_version = models.CharField(max_length=10)
    query_name = models.CharField(max_length=50)
    hit_name = models.CharField(max_length=10)
    query_length = models.PositiveIntegerField(max_length=5)
    query_hsp_start = models.PositiveIntegerField(max_length=5)
    query_hsp_end = models.PositiveIntegerField(max_length=5)
    query_strand = models.CharField(max_length=1)
    query_frame = models.IntegerField(max_length=2)
    hit_length = models.PositiveIntegerField(max_length=5)
    hit_hsp_start = models.PositiveIntegerField(max_length=5)
    hit_hsp_end = models.PositiveIntegerField(max_length=5)
    hit_strand = models.CharField(max_length=1)
    hit_frame = models.IntegerField(max_length=2)
    hsp_score = models.IntegerField(max_length=4)
    hsp_bits = models.FloatField(max_length=10)
    hsp_evalue = models.FloatField(max_length=10)
    hsp_length = models.PositiveIntegerField(max_length=5)
    hsp_gaps = models.PositiveIntegerField(max_length=5)
    hsp_identities = models.PositiveIntegerField(max_length=5)
    hsp_identity_percent = models.FloatField(max_length=6)
    hsp_positives = models.PositiveIntegerField(max_length=5)
    hsp_positive_percent = models.FloatField(max_length=6)
    query_coverage = models.FloatField(max_length=6)
    hit_coverage = models.FloatField(max_length=6)
    hit_description = models.TextField()





# class Refseq(models.Model):
#     accession = models.CharField(max_length=10)
#     seq = models.TextField()
#     species = models.CharField(max_length=15)
#     description = models.TextField()