from datetime import datetime, timedelta

from django.utils import timezone

from Ads_Project.functions import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.db.models import Q

from system.models import User, Tabligh, Click, TablighatMontasherKonande,Payam


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        k = request.user.get_kif_daramad()
        user = request.user
        this_month_clicks = dict(tarikh__month=datetime.now().month)
        this_month_publishes = dict(tarikh__month=datetime.now().month)
        online_time_limite = timezone.now() - timedelta(seconds=600)
        count_user_online = User.objects.filter(last_activity__gte=online_time_limite).count()
        all_User = User.objects.count()
        today = datetime.today()
        all_User_Today = User.objects.filter(date_joined__year=today.year, date_joined__month=today.month, date_joined__day=today.day).count()
        all_tabligh= Tabligh.objects.count()
        if not user.is_superuser:
            this_month_clicks['montasher_konande'] = user
            this_month_publishes['montasher_konande'] = user
        queries = {
            "this_month_clicks": Click.objects.filter(**this_month_clicks).count(),
            "this_month_publishes": TablighatMontasherKonande.objects.filter(**this_month_publishes).count(),
            "all_direct_recieve": k.current_recieved_direct,
            "all_indirect_recieve": k.current_recieved_indirect,
            "count_online_user": count_user_online,
            "all_user":all_User,
            "all_User_Today":all_User_Today,
            "all_tabligh":all_tabligh
        }
        tablighs = Tabligh.objects.filter(vazeyat=1).order_by('-id')[:10]
        message_not_read=Payam.objects.filter(Q(girande=self.request.user),Q(vazeyat=1))

        count_message_not_read=message_not_read.count()
        print('count_message_not_read',count_message_not_read)

        return render(request, 'panel/index/dashboard.html', {'tablighs': tablighs, 'queries': queries,
                                                              'count_message_not_read':count_message_not_read,
                                                              'message_not_read':message_not_read})
