from subprocess import Popen
from django.core.files.temp import NamedTemporaryFile
from Bio.Blast import NCBIXML


def blastn_and_gethitnames(query_path='', db_path='', evalue=1e-5):
    """
    Do blastn and return hit names
    """
    assert query_path and db_path, 'query_path and db_path can not be empty.'

    fo = NamedTemporaryFile(prefix='blastn_')
    blastn_cmd = 'blastn -query {} -db "{}" -evalue {} -outfmt 5 -out {}'.format(query_path,
                                                                                 db_path,
                                                                                 evalue,
                                                                                 fo.name)

    blastn_proc = Popen(blastn_cmd, shell=True)
    blastn_proc.wait()

    blast_records = NCBIXML.parse(fo.file)

    hitnames = []
    for record in blast_records:
        for alignment in record.alignments:
            hitnames.append(alignment.hit_def)

    return hitnames
