from django.utils import translation

from system.models import TanzimatPaye, LANGUGE_SITE


def simple_middleware(get_response):

    def middleware(request):
        t = TanzimatPaye.get_settings(LANGUGE_SITE, 0)
        if t == 1:
            lang = 'fa'
        else:
            lang = 'en'
        translation.activate(lang)
        response = get_response(request)
        return response

    return middleware
