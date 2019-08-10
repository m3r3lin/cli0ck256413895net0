from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
import encodings.base64_codec

from Ads_Project.functions import LoginRequiredMixin
from system.models import User, Tabligh, Click, TablighatMontasherKonande, SODE_MODIR, TanzimatPaye, SATH, \
    COUNT_LEVEL_NETWORK,HistoryIndirect
import simplejson as json


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
        click = Click.objects.create(tabligh=tabligh, montasher_konande=user,
                                     mablagh_har_click=tabligh.mablagh_har_click)
        sode_modir = TanzimatPaye.get_settings(SODE_MODIR)
        max_sath_sod=TanzimatPaye.get_settings(COUNT_LEVEL_NETWORK)

        if user.list_parent is not None:
            jsonDec = json.decoder.JSONDecoder()
            list_parent = jsonDec.decode(user.list_parent)

            for ids,parent in enumerate(list_parent[::-1]):
                if ids+1<=max_sath_sod:
                    parent_user=User.objects.filter(id=parent[0]).first()
                    if parent_user is not None:
                        sode_sath=TanzimatPaye.get_settings(SATH+str(ids+1),0)
                        sode_modir+=sode_sath
                        sod=click.mablagh_har_click*sode_sath/100
                        parent_user.add_to_kif_daramad(sod,direct=False)
                        HistoryIndirect.objects.create(montasher_konande=user, parent=parent_user,
                                                     mablagh=sod)
        user.add_to_kif_daramad(click.mablagh_har_click*(100-sode_modir)/100)

        if user.id != request.user.id:
            tabligh.tedad_click_shode += 1
            tabligh.save()

        return render(request, 'system/Tabligh/Show_Tabligh.html', context={
            "tabligh": tabligh
        })
