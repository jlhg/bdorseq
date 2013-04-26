from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext
from django.db.models import Q
from coffin.shortcuts import render_to_response
from transcriptome.models import Transcript, Refseq
from transcriptome import forms
from scripts import modelformatter, alignment, formatter
import re
import pdb


def index(request):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        return render_to_response('index.jinja2',
                                  {'account_status': 'expired',
                                   'login_form': login_form},
                                  context_instance=RequestContext(request))

    else:
        transcript_search_form = forms.TranscriptSearchForm()
        return render_to_response('index.jinja2',
                                  {'account_status': 'active',
                                   'transcript_search_form': transcript_search_form},
                                  context_instance=RequestContext(request))


@csrf_protect
def signin(request):
    if request.user.is_authenticated():
        transcript_search_form = forms.TranscriptSearchForm()
        return render_to_response('index.jinja2',
                                  {'account_status': 'active',
                                   'transcript_search_form': transcript_search_form},
                                  context_instance=RequestContext(request))

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    transcript_search_form = forms.TranscriptSearchForm()
                    transcript_search_form = forms.TranscriptSearchForm()
                    return render_to_response('index.jinja2',
                                              {'account_status': 'active',
                                               'transcript_search_form': transcript_search_form},
                                              context_instance=RequestContext(request))

                else:
                    login_form = forms.LoginForm()
                    return render_to_response('index.jinja2',
                                              {'account_status': 'inactive',
                                               'login_form': login_form},
                                              context_instance=RequestContext(request))

            else:
                login_form = forms.LoginForm()
                return render_to_response('index.jinja2',
                                          {'account_status': 'invalid',
                                           'login_form': login_form},
                                          context_instance=RequestContext(request))

        else:
            raise Http404


def signout(request):
    logout(request)
    login_form = forms.LoginForm()
    return render_to_response('index.jinja2',
                              {'account_status': 'expired',
                               'login_form': login_form},
                              context_instance=RequestContext(request))


def search(request):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        return render_to_response('index.jinja2',
                                  {'account_status': 'expired',
                                   'login_form': login_form},
                                  context_instance=RequestContext(request))

    else:
        if request.method == 'GET':
            seqname = str(request.GET.get('seqname', '')).strip()
            line = request.GET.get('line', '')
            seq = str(request.GET.get('seq', '')).strip()
            refacc = str(request.GET.get('refacc', '')).strip()
            refdes = str(request.GET.get('refdes', '')).strip()
            order = request.GET.get('order', 'seqname')
            items_per_page = int(request.GET.get('items_per_page', 20))
            page = int(request.GET.get('page', 1))

            transcript_search_form = forms.TranscriptSearchForm(request.GET)

        else:
            raise Http404

        if page < 1:
            page = 1

        search_options = []

        if seqname:
            search_options.append(Q(seqname__icontains=seqname))

        if line:
            search_options.append(Q(line__icontains=line))

        if seq:
            search_options.append(Q(seq__icontains=seq))

        if refacc:
            search_options.append(Q(homology__hit_name_id__icontains=refacc))

        if refdes:
            search_options.append(Q(homology__hit_description__search=refdes))

        transcript_set = Transcript.objects.filter(*search_options).order_by(order)

        pager = {'items_per_page': items_per_page,
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

        if page * items_per_page < search_count:
            # Has next page
            pager['next_page'] = page + 1
            transcript_subset = transcript_set[(page - 1) * pager.get('items_per_page'): page * pager.get('items_per_page')]

        else:
            # Last page
            transcript_subset = transcript_set[(page - 1) * pager.get('items_per_page'): transcript_set.count()]

        return render_to_response('search.jinja2',
                                  {'account_status': 'active',
                                   'transcript_search_form': transcript_search_form,
                                   'transcript_subset': transcript_subset,
                                   'pager': pager,
                                   'getparam': request.GET,
                                   'search_count': search_count},
                                  context_instance=RequestContext(request))


def details(request, seqname):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        return render_to_response('index.jinja2',
                                  {'account_status': 'expired',
                                   'login_form': login_form},
                                  context_instance=RequestContext(request))

    else:
        transcript = Transcript.objects.get(seqname=seqname)

        if not transcript:
            raise Http404

        alignment_protein_html = ''

        if transcript.homology_set.all().exists():
            reference = Refseq.objects.get(accession=transcript.homology_set.all()[0].hit_name_id)

            alignment_protein = alignment.pairwise_protein(transcript.seqname,
                                                           transcript.seq,
                                                           transcript.homology_set.all()[0].query_frame,
                                                           reference.accession,
                                                           reference.seq,
                                                           transcript.homology_set.all()[0].hit_frame)

            alignment_protein_html = formatter.clustal_to_html(alignment_protein, 'a')

        return render_to_response('details.jinja2',
                                  {'transcript': transcript,
                                   'alignment_protein_html': alignment_protein_html},
                                  context_instance=RequestContext(request))


@csrf_exempt
def export(request):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        return render_to_response('index.jinja2',
                                  {'account_status': 'expired',
                                   'login_form': login_form},
                                  context_instance=RequestContext(request))

    else:
        if request.method == 'POST':
            seqname = request.POST.get('seqname', '').strip('/')
            line = request.POST.get('line', '').strip('/')
            seq = request.POST.get('seq', '').strip('/')
            refacc = request.POST.get('refacc', '').strip('/')
            refdes = request.POST.get('refdes', '').strip('/')
            order = request.POST.get('order', 'seqname').strip('/')

            ids = []

            for i in request.POST:
                if re.search('_export_\d+', i):
                    ids.append(request.POST.get(i))

            if ids:
                # Export selected items
                transcript_set = Transcript.objects.filter(id__in=ids).order_by(order)

            else:
                # Export all filterd items
                search_options = []

                if seqname:
                    search_options.append(Q(seqname__icontains=seqname))

                if line:
                    search_options.append(Q(line__icontains=line))

                if seq:
                    search_options.append(Q(seq__icontains=seq))

                if refacc:
                    search_options.append(Q(homology__hit_name_id__icontains=refacc))

                if refdes:
                    search_options.append(Q(homology__hit_description__search=refdes))

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


def adduser(request):
    pass
