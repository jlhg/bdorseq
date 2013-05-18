from subprocess import Popen, PIPE
from django.core.files.temp import NamedTemporaryFile
from Bio.Seq import Seq


def pairwise_dna(seq1, seq2):
    pass


def pairwise_protein(query_name, query_seq, query_frame, subject_name, subject_seq, subject_frame):

    if query_frame < 0:
        query_name = query_name + '(' + str(query_frame) + ')'
        query_seq = Seq(query_seq).reverse_complement()[-query_frame - 1:].translate().tostring()

    elif query_frame > 0:
        query_name = query_name + '(' + str(query_frame) + ')'
        query_seq = Seq(query_seq)[query_frame - 1:].translate().tostring()

    if subject_frame < 0:
        subject_name = subject_name + '(' + str(subject_frame) + ')'
        subject_seq = Seq(subject_seq).reverse_complement()[-subject_frame - 1:].translate().tostring()

    elif subject_frame > 0:
        subject_name = subject_name + '(' + str(subject_frame) + ')'
        subject_seq = Seq(subject_seq)[subject_frame - 1:].translate().tostring()

    input_file = NamedTemporaryFile(prefix='mafft_')
    input_file.write('\n'.join(['>' + query_name,
                                query_seq.upper(),
                                '>' + subject_name,
                                subject_seq.upper()]))
    input_file.flush()

    namelength = max([len(query_name), len(subject_name)]) + 4

    mafft_cmd = 'mafft --preservecase --clustalout --namelength ' + str(namelength) + ' ' + input_file.name
    mafft_proc = Popen(mafft_cmd, stdout=PIPE, stderr=PIPE, shell=True)

    stdout, stderr = mafft_proc.communicate()

    return stdout


def multiple_dna(*args):
    """
    List of tuples: (seq_name, seq_frame, seq)
    """
    seq_name_lengths = []
    input_file = NamedTemporaryFile(prefix='mafft_')

    for arg in args:
        seq_name, seq_frame, seq = arg

        if seq_frame < 0:
            seq_name = seq_name + '(' + str(seq_frame) + ')'

        elif seq_frame > 0:
            seq_name = seq_name + '(' + str(seq_frame) + ')'

        input_file.write('>' + seq_name + '\n' + seq.upper() + '\n')
        seq_name_lengths.append(len(seq_name))

    input_file.flush()

    namelength = max(seq_name_lengths) + 4

    mafft_cmd = 'mafft --preservecase --clustalout --namelength ' + str(namelength) + ' ' + input_file.name
    mafft_proc = Popen(mafft_cmd, stdout=PIPE, stderr=PIPE, shell=True)

    stdout, stderr = mafft_proc.communicate()

    return stdout


def multiple_protein(*args):
    """
    List of tuples: (seq_name, seq_frame, seq)
    """
    seq_name_lengths = []
    input_file = NamedTemporaryFile(prefix='mafft_')

    for arg in args:
        seq_name, seq_frame, seq = arg

        if seq_frame < 0:
            seq_name = seq_name + '(' + str(seq_frame) + ')'
            seq = Seq(seq).reverse_complement()[-seq_frame - 1:].translate().tostring()

        elif seq_frame > 0:
            seq_name = seq_name + '(' + str(seq_frame) + ')'
            seq = Seq(seq)[seq_frame - 1:].translate().tostring()

        input_file.write('>' + seq_name + '\n' + seq.upper() + '\n')

        seq_name_lengths.append(len(seq_name))

    input_file.flush()

    namelength = max(seq_name_lengths) + 4

    mafft_cmd = 'mafft --preservecase --clustalout --namelength ' + str(namelength) + ' ' + input_file.name
    mafft_proc = Popen(mafft_cmd, stdout=PIPE, stderr=PIPE, shell=True)

    input_file.close()

    stdout, stderr = mafft_proc.communicate()

    return stdout
