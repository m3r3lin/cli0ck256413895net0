from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView
import encodings.base64_codec

from Ads_Project.functions import LoginRequiredMixin
from system.models import User, Tabligh, Click, TablighatMontasherKonande


class ClickedOnTablighView(View):
    def get(self, request, enteshartoken):
        enteshartoken = enteshartoken.split('--')
        if len(enteshartoken) > 1:
            user_id = enteshartoken[1]
            if user_id.isdigit():
                user = get_object_or_404(User, pk=int(user_id))
                del user_id
                enteshartoken = enteshartoken[0]
                tabligh = get_object_or_404(Tabligh, random_url=enteshartoken)
                click = Click.objects.create(tabligh=tabligh, montasher_konande=user,
                                             mablagh_har_click=tabligh.mablagh_har_click)

                if user.id != request.user.id:
                    tabligh.tedad_click_shode += 1
                    tabligh.save()
                return redirect(reverse('PreviewTabligh', args=[tabligh.random_url]))
        raise Http404()
