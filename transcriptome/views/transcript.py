from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext
from coffin.shortcuts import render_to_response
from transcriptome.models import Transcript
from transcriptome import forms
from scripts import modelformatter
import re


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
            transcript_search_form = forms.TranscriptSearchForm()

            accession = request.GET.get('accession', '')
            seqname = request.GET.get('seqname', '')
            line = request.GET.get('line', '')
            seq = request.GET.get('seq', '')
            refacc = request.GET.get('refacc', '')
            refdes = request.GET.get('refdes', '')
            order = request.GET.get('order', 'accession')
            items_per_page = int(request.GET.get('items_per_page', 20))
            page = int(request.GET.get('page', 1))

        else:
            raise Http404

        if page < 1:
            page = 1

        transcript_set = Transcript.objects.filter(accession__icontains=accession,
                                                   seqname__icontains=seqname,
                                                   line__icontains=line,
                                                   seq__icontains=seq,
                                                   homology__hit_name__icontains=refacc,
                                                   homology__hit_description__icontains=refdes).order_by(order)

        pager = {'items_per_page': items_per_page,
                 'previous_page': None,
                 'next_page': None,
                 'first_page': None,
                 'last_page': None,
                 'current_page': page
                 }

        search_count = transcript_set.count()

        check_total_page = divmod(search_count, items_per_page)
        if check_total_page[1] == 0:
            pager['last_page'] = check_total_page[0]

        else:
            pager['last_page'] = check_total_page[0] + 1

        if page > 1:
            # Has previous page
            pager['previous_page'] = page - 1
            pager['first_page'] = 1

        if page * items_per_page < pager.get('last_page'):
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


def details(request, accession):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        return render_to_response('index.jinja2',
                                  {'account_status': 'expired',
                                   'login_form': login_form},
                                  context_instance=RequestContext(request))

    else:
        transcript_details = Transcript.objects.get(accession=accession)
        return render_to_response('details.jinja2',
                                  {'transcript_details': transcript_details},
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
            accession = request.POST.get('accession', '').strip('/')
            seqname = request.POST.get('seqname', '').strip('/')
            line = request.POST.get('line', '').strip('/')
            seq = request.POST.get('seq', '').strip('/')
            refacc = request.POST.get('refacc', '').strip('/')
            refdes = request.POST.get('refdes', '').strip('/')
            order = request.POST.get('order', 'accession').strip('/')

            ids = []

            for i in request.POST:
                if re.search('_export_\d+', i):
                    ids.append(request.POST.get(i))

            if ids:
                # Export selected items
                transcript_set = Transcript.objects.filter(id__in=ids).order_by(order)

            else:
                # Export all filterd items
                transcript_set = Transcript.objects.filter(accession__icontains=accession,
                                                           seqname__icontains=seqname,
                                                           line__icontains=line,
                                                           seq__icontains=seq,
                                                           homology__hit_name__icontains=refacc,
                                                           homology__hit_description__icontains=refdes).order_by(order)

            if request.POST.get('export_fasta'):
                # Exports transcript sequences to FASTA file
                response = HttpResponse(modelformatter.transcript_to_fasta(transcript_set), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=%s' % 'transcript.fa'
                return response

            elif request.POST.get('export_tsv'):
                # Exports blast output to TSV format file
                response = HttpResponse(modelformatter.transcript_homology_to_tsv(transcript_set), content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=%s' % 'blast.txt'
                return response

            else:
                raise Http404


def adduser(request):
    pass
