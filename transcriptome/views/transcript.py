import re
import os
from operator import __or__ as OR
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.temp import NamedTemporaryFile
from coffin.shortcuts import render_to_response
from transcriptome.views.decorator import login_checker
from transcriptome.models import Transcript, Refseq
from transcriptome import forms
from scripts import modelformatter, alignment, formatter, blast
import pdb


@login_checker
def index(request):
    archive_search_form = forms.ArchiveSearchForm()
    transcript_search_form = forms.TranscriptSearchForm()
    sequence_variation_search_form = forms.SequenceVariationSearchForm()
    return render_to_response('transcriptome/index.jinja2',
                              {'archive_search_form': archive_search_form,
                               'transcript_search_form': transcript_search_form,
                               'sequence_variation_search_form': sequence_variation_search_form},
                              context_instance=RequestContext(request))


@login_checker
def search(request):
    if request.method == 'GET':
        seqname = str(request.GET.get('seqname', '')).strip()
        line = request.GET.getlist('line', [])
        seq = str(request.GET.get('seq', '')).strip()
        evalue = request.GET.get('evalue', '')
        refacc = str(request.GET.get('refacc', '')).strip()
        refdes = str(request.GET.get('refdes', '')).strip()
        order = request.GET.get('order', 'seqname')
        items_per_page = request.GET.get('items_per_page', 20)
        page = int(request.GET.get('page', 1))

        if not str(items_per_page).isdigit():
            items_per_page = 20
        else:
            items_per_page = int(items_per_page)

        if 'seqname' in request.GET:
            is_search = 1
            transcript_search_form = forms.TranscriptSearchForm(request.GET)
        else:
            is_search = 0
            transcript_search_form = forms.TranscriptSearchForm()
    else:
        raise Http404

    if page < 1:
        page = 1
    else:
        pass

    search_options = []

    if seqname:
        search_options.append(Q(seqname__icontains=seqname))

    if line:
        search_options_line = []
        for i in line:
            search_options_line.append(Q(line=i))
        search_options.append(reduce(OR, search_options_line))
    else:
        # No line is selected, set id = 0 so fetch 'no result'
        search_options.append(Q(id=0))

    if seq:
        try:
            evalue = float(evalue)
        except ValueError:
            # Invalid value, set id = 0 so fetch 'no result'
            search_options.append(Q(id=0))

        fi_seq = NamedTemporaryFile(prefix='seq')
        fi_seq.write('>query\n{}\n'.format(seq))
        fi_seq.flush()

        blastdb_path = []
        for i in line:
            if settings.BLASTDB.get(i):
                blastdb_path.append(os.path.join(settings.BLASTDB_ROOT, settings.BLASTDB.get(i)))
        if blastdb_path:
            hitnames = blast.blastn_and_gethitnames(fi_seq.name, ' '.join(blastdb_path), evalue)
        else:
            hitnames = []

        fi_seq.close()

        if hitnames:
            search_options_seq = []
            for name in hitnames:
                search_options_seq.append(Q(seqname=name))

            search_options.append(reduce(OR, search_options_seq))
        else:
            # No hit is found, set id = 0 so fetch 'no result'
            search_options.append(Q(id=0))

    if refacc:
        search_options.append(Q(homology__hit_name_id__accession__icontains=refacc))

    if refdes:
        search_options.append(Q(homology__hit_description__search=refdes))

    transcript_set = Transcript.objects.filter(*search_options).order_by(order)

    pager = {
        'items_per_page': items_per_page,
        'previous_page': None,
        'next_page': None,
        'first_page': 1,
        'last_page': None,
        'current_page': page
    }

    search_count = transcript_set.count()

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
        transcript_subset = transcript_set[(page - 1) * pager.get('items_per_page'): page * pager.get('items_per_page')]

    else:
        # Last page
        transcript_subset = transcript_set[(page - 1) * pager.get('items_per_page'): transcript_set.count()]

    return render_to_response(
        'transcriptome/search.jinja2',
        {
            'transcript_search_form': transcript_search_form,
            'transcript_subset': transcript_subset,
            'pager': pager,
            'getparam': request.GET,
            'line': line,
            'search_count': search_count,
            'is_search': is_search,
        },
        context_instance=RequestContext(request))


@login_checker
def details(request, seqname):
    try:
        transcript = Transcript.objects.get(seqname=seqname)
    except ObjectDoesNotExist:
        raise Http404

    if transcript.homology_set.all().exists():
        reference = Refseq.objects.get(accession=transcript.homology_set.all()[0].hit_name_id)

        alignment_protein = alignment.pairwise_protein(transcript.seqname,
                                                       transcript.seq,
                                                       transcript.homology_set.all()[0].query_frame,
                                                       reference.accession,
                                                       reference.seq,
                                                       transcript.homology_set.all()[0].hit_frame)

        alignment_protein_html = formatter.clustal_to_html(alignment_protein, 'a')

    else:
        alignment_protein_html = ''

    return render_to_response('transcriptome/details.jinja2',
                              {'transcript': transcript,
                               'alignment_protein_html': alignment_protein_html},
                              context_instance=RequestContext(request))


@csrf_exempt
@login_checker
def export(request):
    if request.method == 'POST':
        seqname = request.POST.get('seqname', '').strip('/')
        line = request.POST.getlist('line', [])
        seq = request.POST.get('seq', '').strip('/')
        evalue = request.GET.get('evalue', '')
        refacc = request.POST.get('refacc', '').strip('/')
        refdes = request.POST.get('refdes', '').strip('/')
        order = request.POST.get('order', 'seqname').strip('/')
        ids = []

        for i in request.POST:
            if re.search('_export_\d+', i):
                ids.append(request.POST.get(i))
            else:
                pass

        if ids:
            # Export selected items
            transcript_set = Transcript.objects.filter(id__in=ids).order_by(order)

        else:
            # Export all filterd items
            search_options = []

            if seqname:
                search_options.append(Q(seqname__icontains=seqname))

            if line:
                search_options_line = []
                for i in line:
                    search_options_line.append(Q(line=i))
                search_options.append(reduce(OR, search_options_line))
            else:
                # No line is selected, set id = 0 so fetch 'no result'
                search_options.append(Q(id=0))

            if seq:
                try:
                    evalue = float(evalue)
                except ValueError:
                    # Invalid value, set id = 0 so fetch 'no result'
                    search_options.append(Q(id=0))

                fi_seq = NamedTemporaryFile(prefix='seq')
                fi_seq.write('>query\n{}\n'.format(seq))
                fi_seq.flush()

                blastdb_path = []
                for i in line:
                    if settings.BLASTDB.get(i):
                        blastdb_path.append(os.path.join(settings.BLASTDB_ROOT, settings.BLASTDB.get(i)))
                if blastdb_path:
                    hitnames = blast.blastn_and_gethitnames(fi_seq.name, ' '.join(blastdb_path), evalue)
                else:
                    hitnames = []

                fi_seq.close()

                if hitnames:
                    search_options_seq = []
                    for name in hitnames:
                        search_options_seq.append(Q(seqname=name))

                    search_options.append(reduce(OR, search_options_seq))
                else:
                    # No hit is found, set id = 0 so fetch 'no result'
                    search_options.append(Q(id=0))

            if refacc:
                search_options.append(Q(homology__hit_name_id__accession__icontains=refacc))

            if refdes:
                search_options.append(Q(homology__hit_description__search=refdes))
            else:
                pass

            transcript_set = Transcript.objects.filter(*search_options).order_by(order)

        if request.POST.get('export_fasta'):
            # Exports transcript sequences to FASTA file
            response = HttpResponse(modelformatter.transcript_to_fasta(transcript_set), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s' % 'transcript.fa'
            return response

        elif request.POST.get('export_blast'):
            # Exports blast output to TSV format file
            response = HttpResponse(modelformatter.transcript_homology_to_blast(transcript_set), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s' % 'blast.txt'
            return response
        elif request.POST.get('export_rpkm'):
            # Exports rpkm data to TSV format file
            response = HttpResponse(modelformatter.transcript_to_expression(transcript_set), content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=%s' % 'expression.txt'
            return response

        else:
            raise Http404
