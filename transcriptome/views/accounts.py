from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from coffin.shortcuts import render_to_response
from transcriptome import forms
from transcriptome.views.decorator import login_checker


@csrf_protect
def signin(request):
    if request.user.is_authenticated():
        next_url = request.GET.get('next', '/bdorseq/')
        return HttpResponseRedirect(next_url)

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(request.POST.get('next', '/bdorseq/'))

                else:
                    login_form = forms.LoginForm()
                    return render_to_response('transcriptome/login.jinja2',
                                              {'login_form': login_form,
                                               'next': request.POST.get('next'),
                                               'account_status': 'inactive'},
                                              context_instance=RequestContext(request))

            else:
                login_form = forms.LoginForm()
                return render_to_response('transcriptome/login.jinja2',
                                          {'login_form': login_form,
                                           'next': request.POST.get('next'),
                                           'account_status': 'invalid'},
                                          context_instance=RequestContext(request))
        else:
            login_form = forms.LoginForm()
            return render_to_response('transcriptome/login.jinja2',
                                      {'login_form': login_form,
                                       'account_status': 'nologin'},
                                      context_instance=RequestContext(request))


@login_checker
def signout(request):
    logout(request)
    return HttpResponseRedirect('/bdorseq/')
