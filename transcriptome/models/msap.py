from django.db import models
from transcriptome.models.transcript import Transcript
from transcriptome.models.refseq import Refseq


class Msap(models.Model):
    msa_method = models.CharField(max_length=10)
    line = models.CharField(max_length=15)
    hit_name = models.ForeignKey(Refseq, to_field='accession')
    ss_name = models.ForeignKey(Transcript, to_field='seqname')
    rs_name = models.ForeignKey(Transcript, to_field='seqname')
    rc_name = models.ForeignKey(Transcript, to_field='seqname')
    mut_num = models.PositiveIntegerField(max_length=4)
    mut_pos = models.CharField(max_length=100)
    mut_profile = models.CharField(max_length=200)
    # block = models.CharField(max_length=200)
    # alignment = models.TextField() # or use real time?

    class Meta:
        app_label = 'transcriptome'
