from subprocess import Popen, PIPE
from django.core.files.temp import NamedTemporaryFile
from Bio.Seq import Seq
from Bio.Align.Applications import MafftCommandline


def pairwise_dna(seq1, seq2):
    pass


def pairwise_protein(query_name, query_seq, query_frame, subject_name, subject_seq, subject_frame):

    if query_frame < 0:
        query_seq = Seq(query_seq).reverse_complement()[-query_frame - 1:].translate().tostring()

    elif query_frame > 0:
        query_seq = Seq(query_seq)[query_frame - 1:].translate().tostring()

    if subject_frame < 0:
        subject_seq = Seq(subject_seq).reverse_complement()[-subject_frame - 1:].translate().tostring()

    elif subject_frame > 0:
        subject_seq = Seq(subject_seq)[subject_frame - 1:].translate().tostring()

    input_file = NamedTemporaryFile(prefix='mafft_')
    input_file.write('\n'.join(['>' + query_name,
                                query_seq,
                                '>' + subject_name,
                                subject_seq]))
    input_file.flush()

    namelength = max([len(query_name), len(subject_name)]) + 4

    mafft_cmd = 'mafft --clustalout --namelength ' + str(namelength) + ' ' + input_file.name
    mafft_proc = Popen(mafft_cmd, stdout=PIPE, stderr=PIPE, shell=True)

    stdout, stderr = mafft_proc.communicate()

    return stdout
