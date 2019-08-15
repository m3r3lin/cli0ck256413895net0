from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
import encodings.base64_codec

from Ads_Project.functions import LoginRequiredMixin
from system.models import User, Tabligh, Click, TablighatMontasherKonande, SODE_MODIR, TanzimatPaye, SATH, \
    COUNT_LEVEL_NETWORK, HistoryIndirect, SoodeTabligh
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
        click = Click()
        click.tabligh = tabligh
        click.montasher_konande = user
        sode_modir = TanzimatPaye.get_settings(SODE_MODIR)
        max_sath_sod = TanzimatPaye.get_settings(COUNT_LEVEL_NETWORK)

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
                                soode_sath = SoodeTabligh.objects.filter(sath=parent_user.sath, tabligh=tabligh).first()
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
            "tabligh": tabligh
        })
