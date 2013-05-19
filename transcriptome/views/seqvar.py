from django.http import Http404, HttpResponseRedirect
from django.db.models import Q
from django.template import RequestContext
from django.core.files.temp import NamedTemporaryFile
from django.core.exceptions import ObjectDoesNotExist
from coffin.shortcuts import render_to_response
from transcriptome import forms
from transcriptome.views.decorator import login_checker
from transcriptome.models import Transcript, Refseq, Msap
from scripts import alignment
from scripts import msaparser


@login_checker
def search(request):
    if request.method == 'GET':
        commonset = request.GET.get('commonset', 'for')
        refacc = str(request.GET.get('refacc', '')).strip()
        refdes = str(request.GET.get('refdes')).strip()
        order = request.GET.get('order', 'accession')
        items_per_page = request.GET.get('items_per_page', 20)
        page = int(request.GET.get('page', 1))

        if not str(items_per_page).isdigit():
            items_per_page = 20
        else:
            items_per_page = int(items_per_page)

        if request.GET.get('commonset'):
            is_search = 1
            sequence_variation_search_form = forms.SequenceVariationSearchForm(request.GET)
        else:
            is_search = 0
            sequence_variation_search_form = forms.SequenceVariationSearchForm()
    else:
        raise Http404

    if page < 1:
        page = 1
    else:
        pass

    search_options = []

    if refacc != '':
        return HttpResponseRedirect('/bdorseq/seqvar/details/%s/%s/' % (commonset, refacc))

    if refdes:
        search_options.append(Q(description__search=refdes))

    commonset_option = {
        'for': Q(commonmutation__formothion=1),
        'fen': Q(commonmutation__fenthion=1),
        'met': Q(commonmutation__methomyl=1),
        'for_fen': Q(commonmutation__for_fen=1),
        'for_met': Q(commonmutation__for_met=1),
        'fen_met': Q(commonmutation__fen_met=1),
        'for_fen_met': Q(commonmutation__for_fen_met=1),
    }

    if commonset_option.get(commonset):
        search_options.append(commonset_option.get(commonset))
        refseqset = Refseq.objects.filter(*search_options).order_by(order)
    else:
        raise Http404

    pager = {'items_per_page': items_per_page,
             'previous_page': None,
             'next_page': None,
             'first_page': 1,
             'last_page': None,
             'current_page': page
             }

    search_count = refseqset.count()

    check_total_page = divmod(search_count, items_per_page)

    if search_count == 0:
        pager['last_page'] = 1

    elif check_total_page[1] == 0:
        pager['last_page'] = check_total_page[0]

    else:
        pager['last_page'] = check_total_page[0] + 1

    if page > 1:
        # Has previous page
        pager['previous_page'] = page - 1
    else:
        pass

    if page * items_per_page < search_count:
        # Has next page
        pager['next_page'] = page + 1
        refseqset = refseqset[(page - 1) * pager.get('items_per_page'): page * pager.get('items_per_page')]

    else:
        # Last page
        refseqset = refseqset[(page - 1) * pager.get('items_per_page'): refseqset.count()]

    return render_to_response('transcriptome/svsearch.jinja2',
                              {'sequence_variation_search_form': sequence_variation_search_form,
                               'refseqset': refseqset,
                               'pager': pager,
                               'getparam': request.GET,
                               'search_count': search_count,
                               'is_search': is_search,
                               },
                              context_instance=RequestContext(request))


@login_checker
def details(request, commonset, refacc):

    # Check if object existed
    search_options = []

    if refacc:
        search_options.append(Q(accession=refacc))

    commonset_option = {
        'for': Q(commonmutation__formothion=1),
        'fen': Q(commonmutation__fenthion=1),
        'met': Q(commonmutation__methomyl=1),
        'for_fen': Q(commonmutation__for_fen=1),
        'for_met': Q(commonmutation__for_fen=1),
        'fen_met': Q(commonmutation__fen_met=1),
        'for_fen_met': Q(commonmutation__for_fen_met=1),
    }

    if commonset_option.get(commonset):
        search_options.append(commonset_option.get(commonset))
        refseqset = Refseq.objects.filter(*search_options)
        if refseqset.count() == 0:
            raise Http404
    else:
        raise Http404

    # Obtain msapset
    msapset = Msap.objects.filter(hit_name=refacc)

    alignment_results = {}
    msaps = {}
    parser_dna = msaparser.Parser()
    parser_protein = msaparser.Parser()

    for insecticide in commonset.split('_'):
        try:
            msap = msapset.get(insecticide=insecticide)
        except ObjectDoesNotExist:
            continue
        else:
            msaps.update({insecticide: msap})

            try:
                ss_transcript = Transcript.objects.get(seqname=msap.ss_name_id)
                rs_transcript = Transcript.objects.get(seqname=msap.rs_name_id)
                rc_transcript = Transcript.objects.get(seqname=msap.rc_name_id)
            except ObjectDoesNotExist:
                raise Http404

            # Executes multiple sequence alignments
            alignment_result_dna = NamedTemporaryFile(prefix='clu_')
            alignment_result_dna.write(alignment.multiple_dna(*[(ss_transcript.seqname,
                                                                 0,
                                                                 ss_transcript.seq),
                                                                (rs_transcript.seqname,
                                                                 0,
                                                                 rs_transcript.seq),
                                                                (rc_transcript.seqname,
                                                                 0,
                                                                 rc_transcript.seq)]))
            alignment_result_dna.flush()
            parser_dna.parse(alignment_result_dna.name, 'n')
            alignment_result_dna.close()

            alignment_result_protein = NamedTemporaryFile(prefix='clu_')
            alignment_result_protein.write(alignment.multiple_protein(*[(ss_transcript.seqname,
                                                                         int(msap.ss_frame),
                                                                         ss_transcript.seq),
                                                                        (rs_transcript.seqname,
                                                                         int(msap.rs_frame),
                                                                         rs_transcript.seq),
                                                                        (rc_transcript.seqname,
                                                                         int(msap.rc_frame),
                                                                         rc_transcript.seq)]))
            alignment_result_protein.flush()
            parser_protein.parse(alignment_result_protein.name, 'a')
            alignment_result_protein.close()

            alignment_results.update({insecticide: (parser_dna.get_clustal_html(),
                                                    parser_protein.get_clustal_html())})

    return render_to_response('transcriptome/svdetails.jinja2',
                              {'msaps': msaps,
                               'commonset': commonset,
                               'refacc': refacc,
                               'refdes': refseqset[0].description,
                               'alignment_results': alignment_results},
                              context_instance=RequestContext(request))
