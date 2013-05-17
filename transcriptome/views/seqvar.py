from operator import __or__ as OR
from django.http import Http404, HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
from coffin.shortcuts import render_to_response
from transcriptome import forms
from transcriptome.views.decorator import login_checker
from transcriptome.models import Msap, CommonMutation, Transcript
from scripts import alignment, formatter


@login_checker
def search(request):
    if request.method == 'GET':
        commonset = request.GET.get('commonset')
        refacc = str(request.GET.get('refacc')).strip()
        order = request.GET.get('order', 'hit_name')
        sequence_variation_search_form = forms.SequenceVariationSearchForm(request.GET)

    else:
        raise Http404

    if refacc:
        HttpResponseRedirect('/seqvar/details/%s/%s/' % (commonset, refacc))

    cs_option = {
        'for': Q(formothion=1),
        'fen': Q(fenthion=1),
        'met': Q(methomyl=1),
    }

    queries = []
    for insecticide in commonset.split('_'):
        queries.append(cs_option.get(insecticide))

    query_set = CommonMutation.objects.filter(*insecticides)

    # for common_mutation in common_mutation_set:
    #     commonset_queries.append(Q(hit_name=common_mutation.hit_name))

    # if commonset_queries:
    #     msap_set = msap_set.objects.filter(reduce(OR, commonset_queries)).order_by(order)
    # else:
    #     msap_set = msap_set.object.order_by(order)

    return render_to_response('transcriptome/seqvar_search.jinja2',
                              {'sequence_variation_search_form': sequence_variation_search_form,
                               'common_mutatoin_set': query_set,
                               'params': request.GET,
                               },
                              context_instance=RequestContext(request))


@login_checker
def details(request, commonset, refacc):
    msap_set = Msap.objects.filter(hit_name=refacc)

    alignment_results = {}
    msaps = {}

    for insecticide in commonset.split('_'):
        try:
            msap = msap_set.objects.get(line_insecticide=insecticide)

        except ObjectDoesNotExist:
            continue

        except:
            msaps.update({insecticide: msap})

            ss_transcript = Transcript.objects.get(seqname=msap.ss_name)
            rs_transcript = Transcript.objects.get(seqname=msap.rs_name)
            rc_transcript = Transcript.objects.get(seqname=msap.rc_name)

            alignment_result_dna = alignment.multiple_dna([(ss_transcript.seqname,
                                                            0,
                                                            ss_transcript.seq),
                                                           (rs_transcript.seqname,
                                                            0,
                                                            rs_transcript.seq),
                                                           (rc_transcript.seqname,
                                                            0,
                                                            rc_transcript.seq)])
            alignment_result_protein = alignment.multiple_protein([(ss_transcript.seqname,
                                                                    ss_transcript.homology.query_frame,
                                                                    ss_transcript.seq),
                                                                   (rs_transcript.seqname,
                                                                    rs_transcript.homology.query_frame,
                                                                    rs_transcript.seq),
                                                                   (rc_transcript.seqname,
                                                                    rc_transcript.homology.query_frame,
                                                                    rc_transcript.seq)])

            alignment_results.update({insecticide: (formatter.clustal_to_html_sv(alignment_result_dna, 'n'),
                                                    formatter.clustal_to_html_sv(alignment_result_protein, 'a'))})

    return render_to_response('transcriptome/svdetails.jinja2',
                              {'msaps': msaps,
                               'alignment_results': alignment_results},
                              context_instance=RequestContext(request))
