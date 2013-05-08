def url(request):
    from django.conf import settings
    return {'FTP_URL': settings.FTP_URL}
