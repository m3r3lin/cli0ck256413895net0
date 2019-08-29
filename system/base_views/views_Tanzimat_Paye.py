import os

from django.contrib import messages
from django.contrib.admindocs.views import TemplateDetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import UpdateView, View, CreateView , FormView,TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django import forms
from django.forms import Form, CharField
from Ads_Project.functions import LoginRequiredMixin
from Ads_Project.settings import BASE_DIR
from system.forms import ActiveCodeMoarefForm, SodeModirForm, sod_modir_max_count_level_FormSetting, \
    some_of_tanzimatpaye_form
from system.forms import (
    Languge_siteForm, Count_level_networkForm, Count_kharid_hadaghalForm, Time_kharid_termForm,
    Taien_meghdar_matlabForm, Show_amarforuserForm, Taied_khodkar_tablighForm, Vahed_poll_siteForm,
    Count_visit_tabligh_Form, Taien_hadaghal_etbarForm, Amar_jaali_Form, MaxNetworkCountForm, LeastBalanceRequiredForm,
    ClickIsChangeAbleForm,PerfectMoneyFormSetting
)
from system.models import TanzimatPaye, ACTIV_MOAREF, LANGUGE_SITE,PERFECT_USER_ID,PERFECT_TITLE,PERFECT_PASSPHRASE
from system.models import (
    VAHED_POLL_SITE, COUNT_LEVEL_NETWORK, SODE_MODIR,
    SHOW_AMAR_FOR_USER, SATH, LEAST_BALANCE_REQUIRED, COUNT_KHARI_HADAGHAL,
    CLICK_IS_CHANGEABLE
)


class ActiveCodeMoarefView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Code_Moaref.html'
    form_class = ActiveCodeMoarefForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=ACTIV_MOAREF, defaults={
            "onvan": ACTIV_MOAREF,
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(ActiveCodeMoarefView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ActiveCodeMoaref')


class ChangeTitlesView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'system/TanzimatPaye/ChangeTitles.html')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "فقط کاربر ادمین اجازه دارد")
            return redirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        for key, data in request.POST.items():
            TanzimatPaye.objects.update_or_create(onvan=key, defaults={
                "onvan": key,
                'value': data,
            })
        if 'website_icon' in request.FILES:
            file = request.FILES.get('website_icon')
            if file.content_type == 'image/png' and file.size < (250 * 1024):
                with open(os.path.join(BASE_DIR, 'static', 'favicon.png'), 'wb+') as opened:
                    opened.write(file.file.read())
            else:
                messages.error(request, _("File type or File size is not right"))

        return redirect(reverse('WebsiteTitle'))


class ClickIsChangeAbleView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/click_is_changeable.html'
    form_class = ClickIsChangeAbleForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=CLICK_IS_CHANGEABLE, defaults={
            "onvan": CLICK_IS_CHANGEABLE,
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(ClickIsChangeAbleView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ClickIsChangeAble')


class LeastBalanceRequiredView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Least_Balance_Required.html'
    form_class = LeastBalanceRequiredForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=LEAST_BALANCE_REQUIRED, defaults={
            "onvan": LEAST_BALANCE_REQUIRED,
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('LeastBalanceRequired')


class SodeModirView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Sode_Modir.html'
    form_class = SodeModirForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=SODE_MODIR, defaults={
            "onvan": SODE_MODIR,
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(SodeModirView, self).form_valid(form)

    def get_success_url(self):
        return reverse('SodeModir')


class Languge_siteView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Languge_site.html'
    form_class = Languge_siteForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=LANGUGE_SITE, defaults={
            "onvan": LANGUGE_SITE,
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Languge_siteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Languge_site')


class Count_Level_networkView2(LoginRequiredMixin, CreateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Count_level_network.html'
    form_class = Count_level_networkForm
    starts_with = SATH

    def form_valid(self, form):
        if "update_sath_network" in self.request.POST:
            if int(form.instance.onvan) > int(TanzimatPaye.get_settings(COUNT_LEVEL_NETWORK, 0)):
                messages.error(self.request, _("Level you exceeds max level"))
                return super(Count_Level_networkView, self).form_invalid(form)

            form.instance.onvan = Count_Level_networkView.starts_with + str(int(form.instance.onvan))
            messages.success(self.request, _("Level is created"))
            t = TanzimatPaye.objects.filter(onvan=form.instance.onvan).first()  # type:TanzimatPaye
            if t:
                t.value = form.instance.value
                t.save()
                return HttpResponseRedirect(self.get_success_url())
        return super(Count_Level_networkView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Count_Level_networkView')


class Count_Level_networkView(LoginRequiredMixin, View):
    starts_with = SATH
    def get(self,request):
        sode_modir, cre = TanzimatPaye.objects.get_or_create(onvan=SODE_MODIR, defaults={
            "onvan": SODE_MODIR,
            'value': 0,
        })
        max_count_level_network, cre = TanzimatPaye.objects.get_or_create(onvan=COUNT_LEVEL_NETWORK, defaults={
            "onvan": COUNT_LEVEL_NETWORK,
            'value': 5,
        })
        sod_form = sod_modir_max_count_level_FormSetting(data={
            "sode_modir":sode_modir.value,
            "had_aksar_count_level":max_count_level_network.value
        })
        levelnetwork_form=Count_level_networkForm
        return render(request, 'system/TanzimatPaye/Count_level_network.html', {'sod_form': sod_form,'form':levelnetwork_form})

    def post(self,request):
        sode_modir, cre = TanzimatPaye.objects.get_or_create(onvan=SODE_MODIR, defaults={
            "onvan": SODE_MODIR,
            'value': 0,
        })
        max_count_level_network, cre = TanzimatPaye.objects.get_or_create(onvan=COUNT_LEVEL_NETWORK, defaults={
            "onvan": COUNT_LEVEL_NETWORK,
            'value': 5,
        })

        if "levelnetwork_form" in self.request.POST:
            form = Count_level_networkForm(request.POST)
            if int(request.POST.get("onvan")) > int(TanzimatPaye.get_settings(COUNT_LEVEL_NETWORK, 0)):
                messages.error(self.request, _("Level you exceeds max level"))
                return self.get(request)
            onvan=request.POST.get("onvan")
            onvan = Count_Level_networkView.starts_with + str(int(onvan))
            messages.success(self.request, _("Level is created"))
            t =  TanzimatPaye.objects.update_or_create(onvan=onvan, defaults={
                "onvan": onvan,
                'value': request.POST.get("value"),
            })
        elif "sod_form" in request.POST:
            sode_modir.value=request.POST.get("sode_modir")
            sode_modir.save()
            max_count_level_network.value=request.POST.get("had_aksar_count_level")
            max_count_level_network.save()
            messages.success(self.request,"بروزرسانی سود مدیر و حداکثر سطح با موفقیت انجام شد.")
        sod_form = sod_modir_max_count_level_FormSetting(data={
            "sode_modir": sode_modir.value,
            "had_aksar_count_level": max_count_level_network.value
        })
        levelnetwork_form = Count_level_networkForm
        return render(request, 'system/TanzimatPaye/Count_level_network.html',
                      {'sod_form': sod_form, 'form': levelnetwork_form})


class Count_Level_networkDataTableView(LoginRequiredMixin, BaseDatatableView):
    model = TanzimatPaye
    columns = ['id', 'onvan', 'value']
    order_columns = ['id', 'onvan', 'value']

    def get_initial_queryset(self):
        qs = super().get_initial_queryset()
        qs = qs.filter(onvan__startswith=Count_Level_networkView.starts_with)
        return qs

    def render_column(self, row, column):
        if column == 'onvan':
            return row.onvan[Count_Level_networkView.starts_with.__len__():]

        return super(Count_Level_networkDataTableView, self).render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(onvan__icontains=search)
        return qs


class Count_Level_networkDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # if request.user.is_administrator:

        Count_Level_network = get_object_or_404(TanzimatPaye, pk=pk)
        print("count_level_network", Count_Level_network)

        Count_Level_network.delete()

        messages.success(self.request, 'سطح موردنظر با موفقیت حذف شد')
        return redirect('Count_Level_networkView')


class Count_Level_networkUpdateView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Update_count_levelnetwork.html'
    form_class = Count_level_networkForm

    def form_valid(self, form):
        count_level_network = form.save(commit=False)

        messages.success(self.request, _("Settings were updated successfully"))
        return super(Count_Level_networkUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Count_Level_networkView')


# class Count_Level_networkView(LoginRequiredMixin, UpdateView):
#     model = TanzimatPaye
#     template_name = 'system/TanzimatPaye/Count_level_network.html'
#     form_class = Count_level_networkForm
#
#     def get_object(self, queryset=None):
#         obj, cre = TanzimatPaye.objects.get_or_create(onvan='count_level_network', defaults={
#             "onvan": 'count_level_network',
#             'value': 0,
#         })
#         return obj
#
#     def form_valid(self, form):
#         messages.success(self.request, _("Settings were updated successfully"))
#         return super(Count_Level_networkView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse('Count_Level_networkView')

class Count_kharid_hadaghalView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Count_kharid_hadaghal.html'
    form_class = Count_kharid_hadaghalForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=COUNT_KHARI_HADAGHAL, defaults={
            "onvan": COUNT_KHARI_HADAGHAL,
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Count_kharid_hadaghalView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Count_kharid_hadaghalView')


class Time_kharid_termView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Time_kharid_term.html'
    form_class = Time_kharid_termForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='time_kharid_term', defaults={
            "onvan": 'time_kharid_term',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Time_kharid_termView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Time_kharid_termView')


class Taien_meghdar_matlabView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Taien_meghdar_matlab.html'
    form_class = Taien_meghdar_matlabForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='taien_meghdar_matlab', defaults={
            "onvan": 'taien_meghdar_matlab',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Taien_meghdar_matlabView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Taien_meghdar_matlabView')


class Show_amar_foruserView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Show_amar_foruser.html'
    form_class = Show_amarforuserForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=SHOW_AMAR_FOR_USER, defaults={
            "onvan": SHOW_AMAR_FOR_USER,
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Show_amar_foruserView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Show_amar_foruserView')


class Taeid_khodkar_tablighView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Taeid_khodkar_tabligh.html'
    form_class = Taied_khodkar_tablighForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='taied_khodkar_tabligh', defaults={
            "onvan": 'taied_khodkar_tabligh',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Taeid_khodkar_tablighView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Taeid_khodkar_tabligh')


class Vahed_poll_siteView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Vahed_poll_site.html'
    form_class = Vahed_poll_siteForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=VAHED_POLL_SITE, defaults={
            "onvan": VAHED_POLL_SITE,
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Vahed_poll_siteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Vahed_poll_site')


class MaxCountNetworkLevel(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Count_level_network_max.html'
    form_class = MaxNetworkCountForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=COUNT_LEVEL_NETWORK, defaults={
            "onvan": COUNT_LEVEL_NETWORK,
            'value': 5,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(MaxCountNetworkLevel, self).form_valid(form)

    def get_success_url(self):
        return reverse('Max_Count_Level_networkView')


class Count_visit_tablighView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Count_visit_tabligh.html'
    form_class = Count_visit_tabligh_Form

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='count_visit_tabligh', defaults={
            "onvan": 'count_visit_tabligh',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Count_visit_tablighView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Count_visit_tabligh')


class Taein_hadaghal_etbarView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Taien_hadaghal_etbar.html'
    form_class = Taien_hadaghal_etbarForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='taein_hadaghal_etbar', defaults={
            "onvan": 'taein_hadaghal_etbar',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, _("Settings were updated successfully"))
        return super(Taein_hadaghal_etbarView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Taein_hadaghal_etbar')


class Amar_jaali_View(LoginRequiredMixin, View):

    def post(self, request):
        count_user_online = self.request.POST.get('count_user_online')
        count_all_user = self.request.POST.get('count_all_user')
        count_user_new_today = self.request.POST.get('count_user_new_today')
        meghdar_daramad_pardahkti = self.request.POST.get('meghdar_daramad_pardahkti')
        count_tabligh_thabti = self.request.POST.get('count_tabligh_thabti')
        print("count_all_user", count_all_user)
        print("count_user_new_today", count_user_new_today)
        print("meghdar_daramad_pardahkti", meghdar_daramad_pardahkti)

        amar_jaali = TanzimatPaye.objects.filter(onvan__startswith='amar_jaali').all()
        print("amar_jalali", amar_jaali)
        for item in amar_jaali:
            if item.onvan == "amar_jaali.count_user_online":
                item.value = count_user_online
                item.save()
            if item.onvan == "amar_jaali.count_all_user":
                item.value = count_all_user
                item.save()
            if item.onvan == "amar_jaali.count_user_new_today":
                item.value = count_user_new_today
                item.save()
            if item.onvan == "amar_jaali.meghdar_daramad_pardahkti":
                item.value = meghdar_daramad_pardahkti
                item.save()
            if item.onvan == "amar_jaali.count_tabligh_thabti":
                item.value = count_tabligh_thabti
                item.save()

        # print("count_user_online",count_user_online)

        count_user_online, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_user_online', defaults={
            "onvan": 'amar_jaali.count_user_online',
            'value': 0,
        })

        count_all_user, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_all_user', defaults={
            "onvan": 'amar_jaali.count_all_user',
            'value': 0,
        })
        count_user_new_today, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_user_new_today',
                                                                     defaults={
                                                                         "onvan": 'amar_jaali.count_user_new_today',
                                                                         'value': 0,
                                                                     })
        meghdar_daramad_pardahkti, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.meghdar_daramad_pardahkti',
                                                                          defaults={
                                                                              "onvan": 'amar_jaali.meghdar_daramad_pardahkti',
                                                                              'value': 0,
                                                                          })
        count_tabligh_thabti, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_tabligh_thabti',
                                                                     defaults={
                                                                         "onvan": 'amar_jaali.count_tabligh_thabti',
                                                                         'value': 0,
                                                                     })
        form = Amar_jaali_Form(data={
            'count_user_online': count_user_online.value,
            'count_all_user': count_all_user.value,
            'count_user_new_today': count_user_new_today.value,
            'meghdar_daramad_pardahkti': meghdar_daramad_pardahkti.value,
            'count_tabligh_thabti': count_tabligh_thabti.value
        })
        messages.success(self.request, _("Settings were updated successfully"))

        return render(request, 'system/TanzimatPaye/Amar_jaali.html', {'form': form})

    def get(self, request):

        count_user_online, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_user_online', defaults={
            "onvan": 'amar_jaali.count_user_online',
            'value': 0,
        })

        count_all_user, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_all_user', defaults={
            "onvan": 'amar_jaali.count_all_user',
            'value': 0,
        })
        count_user_new_today, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_user_new_today',
                                                                     defaults={
                                                                         "onvan": 'amar_jaali.count_user_new_today',
                                                                         'value': 0,
                                                                     })
        meghdar_daramad_pardahkti, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.meghdar_daramad_pardahkti',
                                                                          defaults={
                                                                              "onvan": 'amar_jaali.meghdar_daramad_pardahkti',
                                                                              'value': 0,
                                                                          })
        count_tabligh_thabti, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_tabligh_thabti',
                                                                     defaults={
                                                                         "onvan": 'amar_jaali.count_tabligh_thabti',
                                                                         'value': 0,
                                                                     })
        form = Amar_jaali_Form(data={
            'count_user_online': count_user_online.value,
            'count_all_user': count_all_user.value,
            'count_user_new_today': count_user_new_today.value,
            'meghdar_daramad_pardahkti': meghdar_daramad_pardahkti.value,
            'count_tabligh_thabti': count_tabligh_thabti.value
        })
        # print("form",form)

        return render(request, 'system/TanzimatPaye/Amar_jaali.html', {'form': form})
        # return obj

    def get_success_url(self):
        return reverse('Amar_jaali')


class UpdatePerfectMoneyField(LoginRequiredMixin, FormView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/UpdatePerfectMoneyField.html'
    form_class = PerfectMoneyFormSetting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        PERFECT_USER_ID_VALUE = TanzimatPaye.get_settings(PERFECT_USER_ID, 0)
        PERFECT_TITLE_VALUE = TanzimatPaye.get_settings(PERFECT_TITLE, 0)
        PERFECT_PASSPHRASE_VALUE = TanzimatPaye.get_settings(PERFECT_PASSPHRASE, 0)
        context['form'].fields['PERFECT_USER_ID'].initial=PERFECT_USER_ID_VALUE
        context['form'].fields['PAYEE_NAME'].initial=PERFECT_TITLE_VALUE
        context['form'].fields['Passphrase'].initial=PERFECT_PASSPHRASE_VALUE
        return context

    def form_valid(self, form):

        PERFECT_USER_ID_object, e = TanzimatPaye.objects.update_or_create(onvan=PERFECT_USER_ID, defaults={
                "onvan": PERFECT_USER_ID,
                'value': self.request.POST.get('PERFECT_USER_ID'),
            })
        print(e)
        PERFECT_TITLE_object, e = TanzimatPaye.objects.update_or_create(onvan=PERFECT_TITLE, defaults={
                "onvan": PERFECT_TITLE,
                'value': self.request.POST.get('PAYEE_NAME'),
            })
        print(e)
        PERFECT_PASSPHRASE_object, e = TanzimatPaye.objects.update_or_create(onvan=PERFECT_PASSPHRASE, defaults={
                "onvan": PERFECT_PASSPHRASE,
                'value': self.request.POST.get('Passphrase'),
            })
        print(e)
        messages.success(self.request, _("Settings were updated successfully"))
        return super(UpdatePerfectMoneyField, self).form_valid(form)

    def get_success_url(self):
        return reverse('UpdatePerfectMoneyField')


class some_of_tanzimatpaye_view(LoginRequiredMixin, View):
    def get(self,request):

        click_is_change, cre = TanzimatPaye.objects.get_or_create(onvan=CLICK_IS_CHANGEABLE, defaults={
            "onvan": CLICK_IS_CHANGEABLE,
            'value': 0,
        })

        count_hadaghal_kharid, cre = TanzimatPaye.objects.get_or_create(onvan=COUNT_KHARI_HADAGHAL, defaults={
            "onvan": COUNT_KHARI_HADAGHAL,
            'value': 0,
        })

        hadaghal_meghdar_mojodi, cre = TanzimatPaye.objects.get_or_create(onvan=LEAST_BALANCE_REQUIRED, defaults={
            "onvan": LEAST_BALANCE_REQUIRED,
            'value': 0,
        })

        Taien_Meghdar_Matlab, cre = TanzimatPaye.objects.get_or_create(onvan='taien_meghdar_matlab', defaults={
            "onvan": 'taien_meghdar_matlab',
            'value': 0,
        })

        Taied_Khodkar_Tabligh, cre = TanzimatPaye.objects.get_or_create(onvan='taied_khodkar_tabligh', defaults={
            "onvan": 'taied_khodkar_tabligh',
            'value': 0,
        })
        form = some_of_tanzimatpaye_form(data={
            'taghier_teadad_click':click_is_change.value,
            'hadaghal_teadad_kharid_tabligh':count_hadaghal_kharid.value,
            'hadaghal_meghdar_mojodi':hadaghal_meghdar_mojodi.value,
            'meghdar_matlab':Taien_Meghdar_Matlab.value,
            'taeed_khodkar_tabligh':Taied_Khodkar_Tabligh.value
        })
        return render(request, 'system/TanzimatPaye/some_of_tanzimat_update.html',{'form':form})

    def post(self,request):
        print(request.POST)
        click_is_change, cre = TanzimatPaye.objects.update_or_create(onvan=CLICK_IS_CHANGEABLE, defaults={
            "onvan": CLICK_IS_CHANGEABLE,
            'value': request.POST.get("taghier_teadad_click"),
        })

        count_hadaghal_kharid, cre = TanzimatPaye.objects.update_or_create(onvan=COUNT_KHARI_HADAGHAL, defaults={
            "onvan": COUNT_KHARI_HADAGHAL,
            'value': request.POST.get("hadaghal_teadad_kharid_tabligh"),
        })

        hadaghal_meghdar_mojodi, cre = TanzimatPaye.objects.update_or_create(onvan=LEAST_BALANCE_REQUIRED, defaults={
            "onvan": LEAST_BALANCE_REQUIRED,
            'value': request.POST.get("hadaghal_meghdar_mojodi"),
        })

        Taien_Meghdar_Matlab, cre = TanzimatPaye.objects.update_or_create(onvan='taien_meghdar_matlab', defaults={
            "onvan": 'taien_meghdar_matlab',
            'value': request.POST.get("meghdar_matlab"),
        })

        Taied_Khodkar_Tabligh, cre = TanzimatPaye.objects.update_or_create(onvan='taied_khodkar_tabligh', defaults={
            "onvan": 'taied_khodkar_tabligh',
            'value': request.POST.get("taeed_khodkar_tabligh"),
        })
        return self.get(request)