from coffin.shortcuts import render_to_response


def help(request):
    return render_to_response('help.jinja2', {})
