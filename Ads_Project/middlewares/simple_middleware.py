from django.utils import translation

from system.models import TanzimatPaye, LANGUGE_SITE


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        lang = 'fa'
        original = None
        if translation.LANGUAGE_SESSION_KEY in request.session:
            s_lang = request.session[translation.LANGUAGE_SESSION_KEY]
            translation.activate(s_lang)
            original = s_lang
            lang = s_lang
        else:
            t = TanzimatPaye.get_settings(LANGUGE_SITE, 0)
            if t == 0:
                lang = 'fa'
            else:
                lang = 'en'
        if request.method.lower() == 'get':
            r_lang = request.GET.get('lang', None)
            if r_lang is not None:
                lang = r_lang
        if lang != original:
            translation.activate(lang)
            request.session[translation.LANGUAGE_SESSION_KEY] = lang
        else:
            translation.activate(lang)
        response = get_response(request)
        return response

    return middleware
