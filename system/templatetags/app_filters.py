import os
from datetime import timedelta, datetime

from django import template

from Ads_Project import settings
from Ads_Project.functions import gregorian_to_jalali
from Ads_Project.settings import MAIN_ADMIN_ID
from system.models import (
    TanzimatPaye, TablighatMontasherKonande, User, COUNT_KHARI_HADAGHAL, Tabligh,
    MAX_TIME_TILL_EXPIRE
)

register = template.Library()


@register.filter(name='date_jalali')
def date_jalali(value, mode=1):
    if value is not None:
        if mode == 1:
            date_time = value.astimezone()
            if date_time.minute < 10:
                minute = '0' + str(date_time.minute)
            else:
                minute = str(date_time.minute)
            if date_time.second < 10:
                second = '0' + str(date_time.second)
            else:
                second = str(date_time.second)

            if date_time.hour < 10:
                hour = '0' + str(date_time.hour)
            else:
                hour = str(date_time.hour)
            shamsi = gregorian_to_jalali(date_time.year, date_time.month, date_time.day)
            return "{h}:{m}:{s} {year}/{month}/{day}".format(year=shamsi[0],
                                                             month=shamsi[1],
                                                             day=shamsi[2],
                                                             h=hour,
                                                             m=minute,
                                                             s=second)
        elif mode == 3:
            date_time = value
            shamsi = gregorian_to_jalali(date_time.year, date_time.month, date_time.day)
            return "{year}/{month}/{day}".format(year=shamsi[0] if shamsi[0] > 9 else '0' + str(shamsi[0]),
                                                 month=shamsi[1] if shamsi[1] > 9 else '0' + str(shamsi[1]),
                                                 day=shamsi[2] if shamsi[2] > 9 else '0' + str(shamsi[2]))
        elif mode == 2:
            year, month, day = value.split('-')
            shamsi = gregorian_to_jalali(int(year), int(month), int(day))
            return "{year}/{month}/{day}".format(year=shamsi[0], month=shamsi[1], day=shamsi[2])

        elif mode == 3:
            return " {h}:{m}:{s}".format(h=0,
                                         m=0,
                                         s=0)
    else:
        return "بدون ثبت"


@register.simple_tag
def setting(key, default, if_string_default=False):
    settings = TanzimatPaye.get_settings(key, default)
    if if_string_default and isinstance(settings, str) and settings == '':
        return default
    return settings


@register.simple_tag
def is_publishing(tabligh, user):
    return TablighatMontasherKonande.objects.filter(tabligh=tabligh, montasher_konande=user)


@register.simple_tag
def r(data):
    return data


@register.simple_tag
def is_main_admin(user):
    return user.id == MAIN_ADMIN_ID


@register.filter(name='generate_publish_url')
def generate_publish_url(value, user: User):
    return value + '--' + str(user.id)


@register.simple_tag
def parse_simple_settings(lang, request):
    translated = ''
    if request.user.allow_indirect():
        translated = TanzimatPaye.get_settings(f'{lang}_message_2', '')
    else:
        translated = TanzimatPaye.get_settings(f'{lang}_message_1', '')
    days = TanzimatPaye.get_settings(MAX_TIME_TILL_EXPIRE, 0)
    fifteen_day_ago = datetime.now() - timedelta(days=days)
    print(days, fifteen_day_ago)
    if '%2%' in translated:
        should_buy = TanzimatPaye.get_settings(COUNT_KHARI_HADAGHAL, 0) - \
                     request.user.tabligh_set.filter(vazeyat=1, tarikh_ijad__gte=fifteen_day_ago).count()
        translated = translated.replace('%2%', '<b>{}</b>'.format(str(should_buy)))
    if '%1%' in translated:
        i = Tabligh.objects.filter(code_tabligh_gozaar=request.user,
                                   vazeyat=1,
                                   tarikh_ijad__gte=fifteen_day_ago) \
            .order_by('-tarikh_ijad').first()
        if i:
            how_log = i.tarikh_ijad - fifteen_day_ago
            translated = translated.replace("%1%", how_log.days)
    if '%3%' in translated:
        translated = translated.replace("%3%", days)
    return translated


@register.simple_tag
def favicon_exists():
    return os.path.exists(os.path.join(settings.FAVICON_ADDRESS))
