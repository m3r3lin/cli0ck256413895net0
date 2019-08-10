from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
import encodings.base64_codec

from Ads_Project.functions import LoginRequiredMixin
from system.models import User, Tabligh, Click, TablighatMontasherKonande


class ClickedOnTablighView(View):
    def get(self, request, enteshartoken):
        enteshartoken = enteshartoken.split('--')
        if len(enteshartoken) < 2 or not isinstance(enteshartoken[1], str) \
                or not enteshartoken[1].isdigit():
            raise Http404()

        user_id = enteshartoken[1]
        enteshartoken = enteshartoken[0]

        user = get_object_or_404(User, pk=int(user_id))
        del user_id

        tabligh = get_object_or_404(Tabligh, random_url=enteshartoken)

        if tabligh.vazeyat == 4:
            raise Http404()
        elif tabligh.tedad_click_shode + 1 > tabligh.tedad_click:
            tabligh.vazeyat = 4
            tabligh.save()
            raise Http404()

        click = Click.objects.create(tabligh=tabligh, montasher_konande=user,
                                     mablagh_har_click=tabligh.mablagh_har_click)

        user.add_to_kif_daramad(click.mablagh_har_click)

        if user.id != request.user.id:
            tabligh.tedad_click_shode += 1
            tabligh.save()

        return render(request, 'system/Tabligh/Show_Tabligh.html', context={
            "tabligh": tabligh
        })
