# from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
# from django.db.models import Q
from transcriptome.models import Transcript
from django.http import Http404


def index(request):
    if request.user.is_authenticated():
        return render(request, 'index.html', {'account_status': 'active'})

    else:
        return render(request, 'signin.html', {'account_status': 'expired'})


def signin(request):
    if request.user.is_authenticated():
        return render(request, 'index.html', {'account_status': 'active'})

    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html', {'account_status': 'active'})

                else:
                    return render(request, 'signin.html', {'account_status': 'inactive'})

            else:
                return render(request, 'signin.html', {'account_status': 'invalid'})

        else:
            raise Http404


def search(request):
    if not request.user.is_authenticated():
        return render(request, 'signin.html', {'account_status': 'expired'})

    else:
        if request.method == 'POST':
            transcript_name = request.POST.get('transcript_name')
            insecticide = request.POST.get('insecticide')
            line = request.POST.get('line')
            transcript_seq = request.POST.get('seq')
            refseq_acc = request.POST.get('refacc')
            refseq_des = request.POST.get('refdes')

        elif request.method == 'GET':
            transcript_name = request.GET.get('name', '')
            insecticide = request.GET.get('is', '')
            line = request.GET.get('line', '')
            transcript_seq = request.GET.get('seq', '')
            refseq_acc = request.GET.get('refacc', '')
            refseq_des = request.GET.get('refdes', '')
        else:
            raise Http404

        transcriptset = Transcript.objects.filter(seq_name__icontains=transcript_name,
                                                  insecticide=insecticide,
                                                  line=line,
                                                  seq__search=transcript_seq,
                                                  refseq_acc__icontains=refseq_acc,
                                                  refseq_des__search=refseq_des)

        return render(request, 'search.html', {'transcript_list': transcriptset})


def details(request, transcript_acc):
    pass


def export(request):
    pass


def adduser(request):
    pass
