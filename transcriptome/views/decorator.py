from django.template import RequestContext
from coffin.shortcuts import render_to_response
from transcriptome import forms


def login_checker(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            login_form = forms.LoginForm()
            return render_to_response('login.jinja2',
                                      {'login_form': login_form,
                                       'next': request.get_full_path(),
                                       'account_status': 'nologin'},
                                      context_instance=RequestContext(request))

        else:
            return view_func(request, *args, **kwargs)

    wrap.__doc__ = view_func.__doc__
    wrap.__name__ = view_func.__name__

    return wrap
