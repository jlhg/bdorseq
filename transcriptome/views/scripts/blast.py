from subprocess import Popen
from django.core.files.temp import NamedTemporaryFile
from Bio.Blast import NCBIXML


def blastn(query_path='', db_path='', evalue=1e-5):
    """
    Do blastn and return blast records object
    """
    fo = NamedTemporaryFile(prefix='blastn_')
    blastn_cmd = 'blastn -query {} -db "{}" -evalue {} -out {}'.format(query_path,
                                                                       db_path,
                                                                       evalue,
                                                                       fo.name)
    blastn_proc = Popen(blastn_cmd, shell=True)
    blastn_proc.wait()
    blast_records = NCBIXML.parse(fo.name)
    fo.close()

    return blast_records


def blastn_and_gethit(query_path, db_path, evalue=1e-5):
    blast_records = blastn(query_path, db_path, evalue)

    hitnames = []
    for record in blast_records:
        for alignment in record.alignments:
            hitnames.append(alignment.hit_def)

    return hitnames
