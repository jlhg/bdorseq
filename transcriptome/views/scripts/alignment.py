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
                                '>' + query_name,
                                subject_seq]))
    input_file.flush()

    mafft_cli = MafftCommandline(input=input_file.name, clustalout=True, namelength=40)

    return mafft_cli()[0]
