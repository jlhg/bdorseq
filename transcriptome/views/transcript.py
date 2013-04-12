# from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
# from django.db.models import Q
from django.http import Http404
from transcriptome.models import Transcript
from transcriptome import forms


def index(request):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        return render(request, 'index.jinja2', {'account_status': 'expired',
                                                'login_form': login_form})

    else:
        transcript_search_form = forms.TranscriptSearchForm()
        return render(request, 'index.jinja2', {'account_status': 'active',
                                                'transcript_search_form': transcript_search_form})


def signin(request):
    if request.user.is_authenticated():
        transcript_search_form = forms.TranscriptSearchForm()
        return render(request, 'index.jinja2', {'account_status': 'active',
                                                'transcript_search_form': transcript_search_form})

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.jinja2', {'account_status': 'active'})

                else:
                    login_form = forms.LoginForm()
                    return render(request, 'index.jinja2', {'account_status': 'inactive',
                                                            'login_form': login_form})

            else:
                login_form = forms.LoginForm()
                return render(request, 'index.jinja2', {'account_status': 'invalid',
                                                        'login_form': login_form})

        else:
            raise Http404


def search(request):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        return render(request, 'index.jinja2', {'account_status': 'expired',
                                                'login_form': login_form})

    else:
        if request.method == 'GET':
            transcript_search_form = forms.TranscriptSearchForm(request.GET)

            if 'line_submit' in request.GET:
                # Change search field
                line = request.GET.get('line_submit')

                if line == 'susceptible':
                    transcript_search_form.line.widget.initial = 'susceptible'
                    transcript_search_form.insecticide.widget.as_hidden

                elif line == 'recovered':
                    transcript_search_form.line.widget.initial = 'recovered'
                    transcript_search_form.insecticide.widget.choices = [('All', 'all'),
                                                                         ('Formothion', 'formothion'),
                                                                         ('Fenthion', 'fenthion'),
                                                                         ('Methomyl', 'methomyl')]

                if request.GET.get('page') is None:
                    return render(request, 'index.jinja2', {'account_status': 'active',
                                                            'transcript_search_form': transcript_search_form})

            transcript_name = request.GET.get('transcript_name', '')
            insecticide = request.GET.get('insecticide', '')
            line = request.GET.get('line', '')
            transcript_seq = request.GET.get('seq', '')
            refacc = request.GET.get('refacc', '')
            refdes = request.GET.get('refdes', '')
            order = request.GET.get('order', 'accession')
            items_per_page = request.GET.get('items_per_page', 20)
            page = request.GET.get('page', 1)

        else:
            raise Http404

        pager = {'items_per_page': items_per_page,
                 'previous_page': None,
                 'next_page': None,
                 'first_page': None,
                 'last_page': None,
                 }

        if page < 1:
            page = 1

        transcript_set = Transcript.objects.filter(seq_name__icontains=transcript_name,
                                                   insecticide=insecticide,
                                                   line=line,
                                                   seq__search=transcript_seq,
                                                   homology__hit_name__icontains=refacc,
                                                   homology__hit_description__search=refdes).order_by(order)

        check_total_page = divmod(transcript_set.count(), items_per_page)
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
            transcript_subset = transcript_set[(page) - 1 * pager.get('items_per_page'): page * pager.get('items_per_page')]

        else:
            # Last page
            transcript_subset = transcript_set[(page - 1) * pager.get('items_per_page'): transcript_set.count()]

        return render(request, 'search.jinja2', {'transcript_search_form': transcript_search_form,
                                                 'transcript_subset': transcript_subset,
                                                 'pager': pager})


def details(request, transcript_acc):
    if not request.user.is_authenticated():
        return render(request, 'signin.jinja2', {'account_status': 'expired'})

    else:
        transcript_details = Transcript.objects.get(accession=transcript_acc)
        return render(request, 'details.jinja2', {'transcript_details': transcript_details})


def export(request):
    pass

    if not request.user.is_authenticated():
        return render(request, 'signin.jinja2', {'account_status': 'expired'})

    else:
        # export data
        pass


def adduser(request):
    pass
