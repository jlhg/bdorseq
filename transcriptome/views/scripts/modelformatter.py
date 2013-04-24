def transcript_to_fasta(transcript_objects):
    fasta = []

    for obj in transcript_objects:
        fasta.append('>' + obj.seqname + '\n' + obj.seq + '\n')

    return ''.join(fasta)


def transcript_homology_to_blast(transcript_objects):
    tsv = []

    tsv.append('\t'.join(['tool',
                          'query_name',
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
        if obj.homology_set.all().count() > 0:
            tsv.append('\t'.join(map(str, [obj.homology_set.all()[0].tool,
                                           obj.homology_set.all()[0].query_name_id,
                                           obj.homology_set.all()[0].hit_name,
                                           obj.homology_set.all()[0].query_length,
                                           obj.homology_set.all()[0].query_hsp_start,
                                           obj.homology_set.all()[0].query_hsp_end,
                                           obj.homology_set.all()[0].query_strand,
                                           obj.homology_set.all()[0].query_frame,
                                           obj.homology_set.all()[0].hit_length,
                                           obj.homology_set.all()[0].hit_hsp_start,
                                           obj.homology_set.all()[0].hit_hsp_end,
                                           obj.homology_set.all()[0].hit_strand,
                                           obj.homology_set.all()[0].hit_frame,
                                           obj.homology_set.all()[0].hsp_score,
                                           obj.homology_set.all()[0].hsp_bits,
                                           obj.homology_set.all()[0].hsp_evalue,
                                           obj.homology_set.all()[0].hsp_length,
                                           obj.homology_set.all()[0].hsp_gaps,
                                           obj.homology_set.all()[0].hsp_identities,
                                           obj.homology_set.all()[0].hsp_identity_percent,
                                           obj.homology_set.all()[0].hsp_positives,
                                           obj.homology_set.all()[0].hsp_positive_percent,
                                           obj.homology_set.all()[0].query_coverage,
                                           obj.homology_set.all()[0].hit_coverage,
                                           obj.homology_set.all()[0].hit_description])) +
                       '\n')

    return ''.join(tsv)


def transcript_to_expression(transcript_objects):
    tsv = []

    tsv.append('\t'.join(['Feature ID',
                          'Gene Length',
                          'SS rpkm',
                          'RS rpkm',
                          'RC rpkm',
                          'RS/SS ratio',
                          'RS/RC ratio',
                          'Expression',
                          'Line',
                          'Insecticide',
                          'Annotation']) +
               '\n')

    for obj in transcript_objects:
        if obj.expression_set.all().count() > 0:
            for i in range(obj.expression_set.all().count()):
                if obj.homology_set.all().count() > 0:
                    annotation = obj.homology_set.all()[0].hit_description

                else:
                    annotation = ''

                tsv.append('\t'.join(map(str, [obj.expression_set.all()[i].query_name_id,
                                               len(obj.seq),
                                               obj.expression_set.all()[i].ss_rpkm,
                                               obj.expression_set.all()[i].rs_rpkm,
                                               obj.expression_set.all()[i].rc_rpkm,
                                               obj.expression_set.all()[i].rs_ss_ratio,
                                               obj.expression_set.all()[i].rs_rc_ratio,
                                               obj.expression_set.all()[i].expression,
                                               obj.expression_set.all()[i].line,
                                               obj.expression_set.all()[i].insecticide,
                                               annotation])) +
                           '\n')
        else:
            tsv.append('ssdfdfd')

    return ''.join(tsv)
