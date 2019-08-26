from datetime import datetime, timedelta

from django.db.models import Q, Sum, Count
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from Ads_Project.functions import LoginRequiredMixin
from system.models import (
    User, Tabligh, Click, TablighatMontasherKonande,
    Payam, Infopm, TanzimatPaye, HistoryIndirect, SHOW_AMAR_FOR_USER
)


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        today = datetime.today()

        # All Queries
        prev_thirty_days = datetime.now() - timedelta(days=30)
        # تعداد کل کلیکهای انجام شده در سامانه بر اساس روز نمودار
        prev_thirty_days_clicks = Click.objects.filter(tarikh__lte=datetime.now(), tarikh__gte=prev_thirty_days)
        if not request.user.is_superuser:
            prev_thirty_days_clicks.filter(montasher_konande=request.user)
        prev_thirty_days_clicks = prev_thirty_days_clicks \
            .values('tarikh') \
            .annotate(by_date=TruncDate('tarikh')).values('by_date') \
            .annotate(by_day_count=Count('tarikh')).values('by_date', 'by_day_count')

        # تعداد کل کلیک های امروز
        today_clicks_count = Click.objects.filter(tarikh__year=today.year,
                                                  tarikh__month=today.month,
                                                  tarikh__day=today.day)
        if not request.user.is_superuser:
            today_clicks_count = today_clicks_count.filter(montasher_konande=request.user)
        today_clicks_count = today_clicks_count.count()

        #  تعداد کلیک های دیروز
        prev_day = today - timedelta(days=1)
        prev_day = prev_day
        prev_day_clicks_count = Click.objects.filter(tarikh__year=prev_day.year,
                                                     tarikh__month=prev_day.month,
                                                     tarikh__day=prev_day.day)
        if not request.user.is_superuser:
            prev_day_clicks_count = prev_day_clicks_count.filter(montasher_konande=request.user)
        prev_day_clicks_count = prev_day_clicks_count.count()

        # تعداد کل کلیک ها
        all_clicks_count = Click.objects.all()
        if not request.user.is_superuser:
            all_clicks_count = all_clicks_count.filter(montasher_konande=request.user)
        all_clicks_count = all_clicks_count.count()

        # تعداد کل هزینه های دریافتی بابت کلیک اعضا بر اساس روز نمودار
        prev_thirty_days_income = HistoryIndirect.objects.filter(tarikh__lte=datetime.now(),
                                                                 tarikh__gte=prev_thirty_days)
        if not request.user.is_superuser:
            prev_thirty_days_income = prev_thirty_days_income.filter(montasher_konande=request.user)
        prev_thirty_days_income = prev_thirty_days_income.values('tarikh') \
            .annotate(by_date=TruncDate('tarikh')).values('by_date') \
            .annotate(by_day_count=Sum('mablagh')).values('by_date', 'by_day_count')
        # تعداد کل تبلیغات ایجادا شده امروز
        today_payed_sum = HistoryIndirect.objects.filter(tarikh__year=today.year,
                                                         tarikh__month=today.month,
                                                         tarikh__day=today.day)
        if not request.user.is_superuser:
            today_payed_sum = today_payed_sum.filter(montasher_konande=request.user)
        today_payed_sum = today_payed_sum.aggregate(summed=Sum('mablagh'))['summed']
        today_payed_sum = today_payed_sum if today_payed_sum else 0

        # تعداد کل تبلیغات ایجاد شده دیروز
        prev_day_payed_sum = HistoryIndirect.objects.filter(tarikh__year=prev_day.year,
                                                            tarikh__month=prev_day.month,
                                                            tarikh__day=prev_day.day)
        if not request.user.is_superuser:
            prev_day_payed_sum = prev_day_payed_sum.filter(montasher_konande=request.user)
        prev_day_payed_sum = prev_day_payed_sum.aggregate(summed=Sum('mablagh'))['summed']
        prev_day_payed_sum = prev_day_payed_sum if prev_day_payed_sum else 0

        # تعداد کل تبلیغات ایجاد شده
        all_payed_sum = HistoryIndirect.objects.all()
        if not request.user.is_superuser:
            all_payed_sum = all_payed_sum.filter(montasher_konande=request.user)
        all_payed_sum = all_payed_sum.aggregate(summed=Sum('mablagh'))['summed']
        all_payed_sum = all_payed_sum if all_payed_sum else 0

        # تعداد تبلیغات اخذ شده توسط سامانه بر اساس روز
        prev_thirty_days_ads = Tabligh.objects.filter(tarikh_ijad__lte=datetime.now(),
                                                      tarikh_ijad__gte=prev_thirty_days)

        today_all_ads = Tabligh.objects.filter(tarikh_ijad__year=today.year,
                                               tarikh_ijad__month=today.month,
                                               tarikh_ijad__day=today.day).count()

        prev_day_all_ads = Tabligh.objects.filter(tarikh_ijad__year=prev_day.year,
                                                  tarikh_ijad__month=prev_day.month,
                                                  tarikh_ijad__day=prev_day.day).count()
        all_ads_count = Tabligh.objects.count()

        prev_thirty_days_ads = prev_thirty_days_ads.values('tarikh_ijad') \
            .annotate(by_date=TruncDate('tarikh_ijad')).values('by_date') \
            .annotate(by_day_count=Count('tarikh_ijad')).values('by_date', 'by_day_count')

        # تعداد زیر مجموعه ها بر اساس سطح نمودار
        all_referrals = User.objects \
            .filter(date_joined__lte=datetime.now(), date_joined__gte=prev_thirty_days) \
            .filter(list_parent__contains=f'[{request.user.id}]').values("sath") \
            .annotate(tedad_sath=Count("sath"), date_joined_dated=TruncDate("date_joined")) \
            .values('tedad_sath', "date_joined_dated", "sath")
        # این بخش بری تبدیل داده ها بشکلی است که
        # بتوان آنهارا در نمودار های استفاده کرد
        leveled_referrals = {}

        def convert_to_readable(dasdate):
            return f'{dasdate.year}' \
                   f'-{dasdate.month if dasdate.month > 10 else f"0{dasdate.month}"}' \
                   f'-{dasdate.day if dasdate.day > 10 else f"0{dasdate.day}"}'

        for referrals in all_referrals:
            converted = convert_to_readable(referrals['date_joined_dated'])
            if converted in leveled_referrals:
                leveled_referrals[converted][f'level_{referrals["sath"]}'] = referrals["tedad_sath"]
            else:
                leveled_referrals[converted] = {
                    f'level_{referrals["sath"]}': referrals["tedad_sath"]
                }
        # تعداد زیر مجموعه ها امروز
        today_all_referrals = User.objects \
            .filter(date_joined__year=today.year,
                    date_joined__month=today.month,
                    date_joined__day=today.day) \
            .filter(list_parent__contains=f'[{request.user.id}]').count()
        # تعداد زیر مجموعه ها دیروز
        prev_day_all_referrals = User.objects \
            .filter(date_joined__year=prev_day.year,
                    date_joined__month=prev_day.month,
                    date_joined__day=prev_day.day) \
            .filter(list_parent__contains=f'[{request.user.id}]').count()
        # تعداد کل زیر مجموعه ها
        all_referrals_count = User.objects \
            .filter(list_parent__contains=f'[{request.user.id}]').count()
        # User Queries

        # Admin queries
        this_month_clicks = dict(tarikh__month=datetime.now().month)
        this_month_publishes = dict(tarikh__month=datetime.now().month)
        online_time_limite = timezone.now() - timedelta(seconds=600)
        count_user_online = User.objects.filter(
            last_activity__gte=online_time_limite).count()
        all_User = User.objects.count()
        all_User_Today = User.objects.filter(date_joined__year=today.year,
                                             date_joined__month=today.month,
                                             date_joined__day=today.day).count()
        all_tabligh = Tabligh.objects.count()
        all_InfoPm = Infopm.objects.filter(is_active=True).all()
        amar_jali = TanzimatPaye.objects.filter(
            onvan__startswith='amar_jaali').all()
        active_show_forosh = TanzimatPaye.get_settings(SHOW_AMAR_FOR_USER, 0)
        direct_today = Click.objects.filter(montasher_konande=user,
                                            tarikh__year=today.year,
                                            tarikh__month=today.month,
                                            tarikh__day=today.day).aggregate(
            Sum('mablagh_har_click'))
        indirect_today = HistoryIndirect.objects.filter(parent=user,
                                                        tarikh__year=today.year,
                                                        tarikh__month=today.month,
                                                        tarikh__day=today.day).aggregate(Sum('mablagh'))

        if indirect_today['mablagh__sum'] is None:
            indirect_today['mablagh__sum'] = 0
        if direct_today['mablagh_har_click__sum'] is None:
            direct_today['mablagh_har_click__sum'] = 0
        for item in amar_jali:
            if item.onvan == "amar_jaali.count_user_online":
                count_user_online += int(item.value)
            if item.onvan == "amar_jaali.count_all_user":
                all_User += int(item.value)
            if item.onvan == "amar_jaali.count_user_new_today":
                all_User_Today += int(item.value)
            if item.onvan == "amar_jaali.count_tabligh_thabti":
                all_tabligh += int(item.value)

        today_midnight = datetime(today.year, today.month, today.day, 23, 59, 59)
        last_day_morning = today_midnight - timedelta(days=5, hours=23, minutes=59, seconds=59)
        past_five_days_click = Click.objects.filter(
            tarikh__lte=today_midnight,
            tarikh__gte=last_day_morning,
        )
        if not request.user.is_superuser:
            past_five_days_click = past_five_days_click.filter(montasher_konande=request.user)
        past_five_days_click = past_five_days_click.annotate(by_day=TruncDate('tarikh')) \
            .values('by_day').annotate(by_day_count=Count('id')) \
            .values('by_day', 'by_day_count')

        a = str(past_five_days_click.query)
        by_country = User.objects.filter(country__isnull=False) \
            .annotate(count_user_online_country=Count("country")).values('country', 'count_user_online_country')

        if not user.is_superuser:
            this_month_clicks['montasher_konande'] = user
            this_month_publishes['montasher_konande'] = user

        income_pocket = request.user.get_kif_daramad()
        queries = {
            "this_month_clicks": Click.objects.filter(
                **this_month_clicks).count(),
            "this_month_publishes": TablighatMontasherKonande.objects.filter(
                **this_month_publishes).count(),
            "all_direct_recieve": income_pocket.current_recieved_direct,
            "all_indirect_recieve": income_pocket.current_recieved_indirect,
            "count_online_user": count_user_online,
            "count_online_user_by_country": by_country,
            "all_user": all_User,
            "all_User_Today": all_User_Today,
            "all_tabligh": all_tabligh,
            "all_infopm": all_InfoPm,
            "todaynow": datetime.now(),
            "active_show_forosh": active_show_forosh,
            "past_five_days_click": past_five_days_click,
            "all_recive": income_pocket.current_recieved_direct + income_pocket.current_recieved_indirect,
            "today_direct": direct_today['mablagh_har_click__sum'],
            "today_indirect": indirect_today['mablagh__sum'],
            "today_daramad": direct_today['mablagh_har_click__sum'] +
                             indirect_today['mablagh__sum']
            ,
            "clicks": {
                "prev_thirty_days_clicks": prev_thirty_days_clicks,
                "today_clicks_count": today_clicks_count,
                "prev_day_clicks_count": prev_day_clicks_count,
                "all_clicks_count": all_clicks_count,
            },
            "payed": {
                "prev_thirty_days_income": prev_thirty_days_income,
                "today_payed_sum": today_payed_sum,
                "prev_day_payed_sum": prev_day_payed_sum,
                "all_payed_sum": all_payed_sum,
            },
            "ads": {
                "prev_thirty_days_ads": prev_thirty_days_ads,
                "today_all_ads": today_all_ads,
                "prev_day_all_ads": prev_day_all_ads,
                "all_ads_count": all_ads_count,
            },
            "refs": {
                "all_referrals": leveled_referrals,
                "today_all_referrals": today_all_referrals,
                "prev_day_all_referrals": prev_day_all_referrals,
                "all_referrals_count": all_referrals_count,
            },
        }

        tablighs = Tabligh.objects.filter(vazeyat=1).order_by('-id')[:10]
        message_not_read = Payam.objects.filter(Q(girande=self.request.user),
                                                Q(vazeyat=1))

        count_message_not_read = message_not_read.count()

        return render(request, 'panel/index/dashboard.html',
                      {'tablighs': tablighs, 'queries': queries,
                       'count_message_not_read': count_message_not_read,
                       'message_not_read': message_not_read
                       })
