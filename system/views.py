from datetime import datetime

from Ads_Project.functions import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from system.models import User, Tabligh, Click, TablighatMontasherKonande


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        k = request.user.get_kif_daramad()
        user = request.user
        this_month_clicks = dict(tarikh__month=datetime.now().month)
        this_month_publishes = dict(tarikh__month=datetime.now().month)
        if not user.is_superuser:
            this_month_clicks['montasher_konande'] = user
            this_month_publishes['montasher_konande'] = user

        queries = {
            "this_month_clicks": Click.objects.filter(**this_month_clicks).count(),
            "this_month_publishes": TablighatMontasherKonande.objects.filter(**this_month_publishes).count(),
            "all_direct_recieve": k.current_recieved_direct,
            "all_indirect_recieve": k.current_recieved_indirect,
        }
        tablighs = Tabligh.objects.filter(vazeyat=1).order_by('-id')[:10]

        return render(request, 'panel/index/dashboard.html', {'tablighs': tablighs, 'queries': queries})
