from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import Http404
from jinja2 import Environment, PackageLoader
from transcriptome.models import Transcript
from transcriptome import forms

env = Environment(loader=PackageLoader('transcriptome', 'templates'))


def index(request):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        template_index = env.get_template('index.jinja2')
        return HttpResponse(template_index.render({'account_status': 'expired',
                                                   'login_form': login_form}))

    else:
        transcript_search_form = forms.TranscriptSearchForm()
        template_index = env.get_template('index.jinja2')
        return HttpResponse(template_index.render({'account_status': 'active',
                                                   'transcript_search_form': transcript_search_form}))


def signin(request):
    if request.user.is_authenticated():
        transcript_search_form = forms.TranscriptSearchForm()
        template_index = env.get_template('index.jinja2')
        return HttpResponse(template_index.render({'account_status': 'active',
                                                   'transcript_search_form': transcript_search_form}))

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    transcript_search_form = forms.TranscriptSearchForm()
                    template_index = env.get_template('index.jinja2')
                    return HttpResponse(template_index.render({'account_status': 'active',
                                                               'transcript_search_form': transcript_search_form}))

                else:
                    login_form = forms.LoginForm()
                    template_index = env.get_template('index.jinja2')
                    return HttpResponse(template_index.render({'account_status': 'inactive',
                                                              'login_form': login_form}))

            else:
                login_form = forms.LoginForm()
                template_index = env.get_template('index.jinja2')
                return HttpResponse(template_index.render({'account_status': 'inavalid',
                                                          'login_form': login_form}))

        else:
            raise Http404


def search(request):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        template_index = env.get_template('index.jinja2')
        return HttpResponse(template_index.render({'account_status': 'expired',
                                                  'login_form': login_form}))

    else:
        if request.method == 'GET':
            transcript_search_form = forms.TranscriptSearchForm()

            accession = request.GET.get('accession', '')
            seqname = request.GET.get('seqname', '')
            line = request.GET.get('line', 'all')
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

        template_search = env.get_template('search.jinja2')
        return HttpResponse(template_search.render({'account_status': 'active',
                                                    'transcript_search_form': transcript_search_form,
                                                    'transcript_subset': transcript_subset,
                                                    'pager': pager}))


def details(request, accession):
    if not request.user.is_authenticated():
        login_form = forms.LoginForm()
        template_index = env.get_template('index.jinja2')
        return HttpResponse(template_index.render({'account_status': 'expired',
                                                  'login_form': login_form}))

    else:
        transcript_details = Transcript.objects.get(accession=accession)
        template_details = env.get_template('details.jinja2')
        return HttpResponse(template_details.render({'transcript_details': transcript_details}))


def export(request):
    pass


def adduser(request):
    pass
