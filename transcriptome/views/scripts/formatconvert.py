def model_to_fasta(transcript_objects):
    fasta = []
    for obj in transcript_objects:
        fasta.append('>' + obj.seqname + '\n' + obj.seq + '\n')

    return ''.join(fasta)
