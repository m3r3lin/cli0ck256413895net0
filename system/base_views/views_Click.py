import simplejson as json
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from system.functions import get_client_ip
from system.models import (
    User, Tabligh, Click, SODE_MODIR, TanzimatPaye,
    COUNT_LEVEL_NETWORK, HistoryIndirect, SoodeTabligh
)
from system.templatetags.app_filters import date_jalali


class ClickedOnTablighView(View):
    def get(self, request, enteshartoken):
        enteshartoken = enteshartoken.split('--')
        if len(enteshartoken) < 2 or not isinstance(enteshartoken[1], str) \
                or not enteshartoken[1].isdigit():
            raise Http404()

        user_id = enteshartoken[1]
        enteshartoken = enteshartoken[0]

        tabligh = get_object_or_404(Tabligh, random_url=enteshartoken)

        if tabligh.vazeyat == 4:
            raise Http404()
        elif tabligh.tedad_click_shode + 1 > tabligh.tedad_click:
            tabligh.vazeyat = 4
            tabligh.save()
            raise Http404()
        user = get_object_or_404(User, pk=int(user_id))
        del user_id
        click = Click()
        click.tabligh = tabligh
        click.montasher_konande = user
        click.ip = get_client_ip(request)
        sode_modir = TanzimatPaye.get_settings(SODE_MODIR, 0)
        max_sath_sod = TanzimatPaye.get_settings(COUNT_LEVEL_NETWORK, 0)

        # get sath user
        tabligh_first_sath = SoodeTabligh.objects.filter(Q(sath__lte=user.sath) & ~Q(sath=0)).order_by('-sath').first()
        if tabligh_first_sath:
            tabligh_first_sath_sood = tabligh_first_sath.soode_mostaghim
            tabligh_first_sath = tabligh_first_sath.sath
            user.add_to_kif_daramad(tabligh_first_sath_sood, direct=True)
            click.mablagh_har_click = tabligh_first_sath_sood
            click.save()
            # if soode_sath:
            #     User.objects.filter(is_superuser=True).first().add_to_kif_pool(soode_sath.soode_mostaghim)
            if user.list_parent is not None:
                jsonDec = json.decoder.JSONDecoder()
                list_parent = jsonDec.decode(user.list_parent)

                for ids, parent in enumerate(list_parent):
                    if ids + 1 <= max_sath_sod:
                        parent_user = User.objects.filter(id=parent[0]).first()
                        if parent_user.sath < tabligh_first_sath:
                            if parent_user is not None:
                                soode_sath = SoodeTabligh.objects.filter(sath=parent_user.sath,
                                                                         tabligh=tabligh).first()
                                if soode_sath:
                                    parent_user.add_to_kif_daramad(soode_sath.soode_gheire_mostaghim, direct=False)
                                    HistoryIndirect.objects.create(montasher_konande=user, parent=parent_user,
                                                                   mablagh=soode_sath.soode_gheire_mostaghim)
            else:
                soode_sath = SoodeTabligh.objects.filter(sath=1, tabligh=tabligh).first()
                if soode_sath:
                    user.add_to_kif_daramad(soode_sath.soode_mostaghim, direct=True)
        else:
            click.mablagh_har_click = tabligh_first_sath.mablagh_har_click
            click.save()
        if user.id != request.user.id:
            tabligh.tedad_click_shode += 1
            tabligh.save()

        return render(request, 'system/Tabligh/Show_Tabligh.html', context={
            "tabligh": tabligh,
            "montasher_konande": user,
        })


class ShowClick(LoginRequiredMixin, TemplateView):
    template_name = 'system/moshahede/list_of_click.html'


class ClickDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = Click
    columns = ['id', 'montasher_konande', 'tarikh', 'tabligh', 'mablagh_har_click', 'ip']

    def render_column(self, row, column):
        if column == 'tarikh':
            return date_jalali(row.tarikh)
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        qs = qs.filter(Q(tabligh__onvan__icontains=search)
                       | Q(montasher_konande__username__icontains=search)
                       | Q(ip__icontains=search))
        return qs
