from operator import __or__ as OR
from django.http import Http404
from django.db.models import Q
from django.template import RequestContext
from coffin.shortcuts import render_to_response
from transcriptome import forms
from transcriptome.views.decorator import login_checker
from transcriptome.models import Msap, CommonMutation


@login_checker
def search(request):
    if request.method == 'GET':
        commonset = request.GET.get('commonset', '')
        refacc = str(request.GET.get('refacc', '')).strip()
        order = request.GET.get('order', 'hit_name')
        sequence_variation_search_form = forms.SequenceVariationSearchForm(request.GET)

    else:
        raise Http404

    if refacc:
        msap_set = Msap.objects.filter(hit_name_id=refacc)
    else:
        msap_set = Msap.objects.all()

    search_msap_from_commonset = []

    if commonset:
        queries = commonset.split('_')

        search_common_mutation_queries = []
        for query in queries:
            if query == 'for':
                search_common_mutation_queries.append(Q(formothion=1))
            elif query == 'fen':
                search_common_mutation_queries.append(Q(fenthion=1))
            elif query == 'met':
                search_common_mutation_queries.append(Q(methomyl=1))
            else:
                pass

        common_mutation_set = CommonMutation.objects.filter(**search_common_mutation_queries)

        for common_mutation in common_mutation_set:
            search_msap_from_commonset.append(Q(hit_name=common_mutation.hit_name))
    else:
        pass

    if len(search_msap_from_commonset) > 0:
        msap_set = msap_set.objects.filter(reduce(OR, search_msap_from_commonset)).order_by(order)
    else:
        msap_set = msap_set.object.order_by(order)

    return render_to_response('transcriptome/seqvar_search.jinja2',
                              {'sequence_variation_search_form': sequence_variation_search_form,
                               'msap_set': msap_set,
                               'params': request.GET},
                              context_instance=RequestContext(request))
