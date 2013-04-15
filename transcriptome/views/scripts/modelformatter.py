def transcript_to_fasta(transcript_objects):
    fasta = []

    for obj in transcript_objects:
        fasta.append('>' + obj.seqname + '\n' + obj.seq + '\n')

    return ''.join(fasta)


def transcript_homology_to_tsv(transcript_objects):
    tsv = []

    tsv.append('# Tool: ' + transcript_objects[0].homology.tool + '\n')
    tsv.append('\t'.join(['query_name',
                          'hit_name',
                          'query_length',
                          'query_hsp_start',
                          'query_hsp_end',
                          'query_starnd',
                          'query_frame',
                          'hsp_score',
                          'hsp_bits',
                          'hsp_evalue',
                          'hsp_length',
                          'hsp_gaps',
                          'hsp_identities',
                          'hsp_identity_percent',
                          'hsp_positives',
                          'hsp_positive_percent',
                          'query_coverage',
                          'hit_coverage',
                          'hit_description']) +
               '\n')

    for obj in transcript_objects:
        tsv.append('\t'.join(map(str, [obj.homology.query_name_id,
                                       obj.homology.hit_name,
                                       obj.homology.query_length,
                                       obj.homology.query_hsp_start,
                                       obj.homology.query_hsp_end,
                                       obj.homology.query_strand,
                                       obj.homology.query_frame,
                                       obj.homology.hit_length,
                                       obj.homology.hit_hsp_start,
                                       obj.homology.hit_hsp_end,
                                       obj.homology.hit_strand,
                                       obj.homology.hit_frame,
                                       obj.homology.hsp_score,
                                       obj.homology.hsp_bits,
                                       obj.homology.hsp_evalue,
                                       obj.homology.hsp_length,
                                       obj.homology.hsp_gaps,
                                       obj.homology.hsp_identities,
                                       obj.homology.hsp_identity_percent,
                                       obj.homology.hsp_positives,
                                       obj.homology.hsp_positive_percent,
                                       obj.homology.query_coverage,
                                       obj.homology.hit_coverage,
                                       obj.homology.hit_description])) +
                   '\n')

    return ''.join(tsv)
