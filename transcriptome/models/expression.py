from django.db import models
from transcriptome.models.transcript import Transcript


class Expression(models.Model):
    tool = models.CharField(max_length=15)
    query_name = models.ForeignKey(Transcript, to_field='seqname', unique=True)
    ss_rpkm = models.FloatField(max_length=10)
    rs_rpkm = models.FloatField(max_length=10)
    rc_rpkm = models.FloatField(max_length=10)
    rs_ss_ratio = models.FloatField(max_length=10)
    rs_rc_ratio = models.FloatField(max_length=10)
    expression = models.CharField(max_length=5)
    line = models.CharField(max_length=15)
    insecticide = models.CharField(max_length=20)

    class Meta:
        app_label = 'transcriptome'
