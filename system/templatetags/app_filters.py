from django import template

from Ads_Project.functions import gregorian_to_jalali

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
            return "{year}/{month}/{day}".format(year=shamsi[0],
                                                             month=shamsi[1],
                                                             day=shamsi[2])
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
