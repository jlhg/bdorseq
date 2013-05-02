import re
from django.http import Http404
from transcriptome import forms
from coffin.shortcuts import render_to_response
from django.template import RequestContext
from transcriptome.views.decorator import login_checker
from transcriptome.models import Transcript, Refseq, Homology
from scripts import alignment, formatter
import pdb


@login_checker
def search(request):
    if request.method == 'GET':
        line = request.GET.get('line', '')
        refacc = str(request.GET.get('refacc', '')).strip()
        # order = request.GET.get('order', 'seqname')

        if request.GET.get('align_selected'):
            align_type = 'include'

        elif request.GET.get('align_unselected'):
            align_type = 'exclude'

        else:
            align_type = 'all'

        if align_type == 'include' or align_type == 'exclude':
            homo_ids = []

            for i in request.GET:
                if re.search('homo_\d+', i):
                    homo_ids.append(int(request.GET.get(i)))

            if not homo_ids:
                # No selected items
                align_type = 'all'

        archive_search_form = forms.ArchiveSearchForm(request.GET)

    else:
        raise Http404

    homology_set = Homology.objects.filter(hit_name_id=refacc).order_by('query_name')

    # Store selection information of homology objects
    select_status = {}

    if homology_set.exists():
        refseq = Refseq.objects.get(accession=refacc)

        align_dna_set = []
        align_protein_set = []
        homology_subset = []

        align_protein_set.append((refseq.accession, 0, refseq.seq))

        for homology in homology_set:
            transcript = Transcript.objects.get(seqname=homology.query_name_id)

            if transcript.line == line:
                homology_subset.append(homology)

                if align_type == 'include':
                    if homology.id in homo_ids:
                        align_dna_set.append((transcript.seqname, homology.query_frame, transcript.seq))
                        align_protein_set.append((transcript.seqname, homology.query_frame, transcript.seq))
                        select_status.update({homology.id: 1})
                    else:
                        select_status.update({homology.id: 0})

                elif align_type == 'exclude':
                    if homology.id not in homo_ids:
                        align_dna_set.append((transcript.seqname, homology.query_frame, transcript.seq))
                        align_protein_set.append((transcript.seqname, homology.query_frame, transcript.seq))
                        select_status.update({homology.id: 1})
                    else:
                        select_status.update({homology.id: 0})

                else:
                    align_dna_set.append((transcript.seqname, homology.query_frame, transcript.seq))
                    align_protein_set.append((transcript.seqname, homology.query_frame, transcript.seq))
                    select_status.update({homology.id: 1})

        if not align_dna_set:
            # No matched results
            return render_to_response('transcriptome/archive.jinja2',
                                      {'archive_search_form': archive_search_form,
                                       'params': request.GET},
                                      context_instance=RequestContext(request))
        else:
            # Run multiple sequence alignments
            if len(align_dna_set) > 1:
                multiple_dna_alignment = alignment.multiple_dna(*align_dna_set)
                multiple_dna_alignment_html = formatter.clustal_to_html(multiple_dna_alignment, 'n')
            else:
                multiple_dna_alignment_html = ''

            multiple_protein_alignment = alignment.multiple_protein(*align_protein_set)
            multiple_protein_alignment_html = formatter.clustal_to_html(multiple_protein_alignment, 'a')

            return render_to_response('transcriptome/archive.jinja2',
                                      {'archive_search_form': archive_search_form,
                                       'select_status': select_status,
                                       'homology_subset': homology_subset,
                                       'multiple_dna_alignment_html': multiple_dna_alignment_html,
                                       'multiple_protein_alignment_html': multiple_protein_alignment_html,
                                       'params': request.GET},
                                      context_instance=RequestContext(request))

    else:
        # No matched results
        return render_to_response('transcriptome/archive.jinja2',
                                  {'archive_search_form': archive_search_form,
                                   'params': request.GET},
                                  context_instance=RequestContext(request))
