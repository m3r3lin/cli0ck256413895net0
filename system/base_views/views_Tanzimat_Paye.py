from django.contrib import messages
from django.urls import reverse
from django.views.generic import UpdateView, View, FormView, CreateView
from django.shortcuts import render, get_object_or_404, redirect
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from system.forms import ActiveCodeMoarefForm, SodeModirForm,\
    Languge_siteForm,Count_level_networkForm,Count_kharid_hadaghalForm,Time_kharid_termForm,\
    Taien_meghdar_matlabForm,Show_amarforuserForm,Taied_khodkar_tablighForm,Vahed_poll_siteForm,\
    Count_visit_tabligh_Form,Taien_hadaghal_etbarForm,Amar_jaali_Form

from system.models import TanzimatPaye, ACTIV_MOAREF
from system.forms import ActiveCodeMoarefForm, SodeModirForm, TedadSathShabakeForm
from system.models import TanzimatPaye, ACTIV_MOAREF, TEDAD_SATH_SHABAKE


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
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(ActiveCodeMoarefView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ActiveCodeMoaref')


class TedadSathShabakeView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Tedad_Sath_Shabake.html'
    form_class = TedadSathShabakeForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan=TEDAD_SATH_SHABAKE, defaults={
            "onvan": TEDAD_SATH_SHABAKE,
            'value': 1,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(TedadSathShabakeView, self).form_valid(form)

    def get_success_url(self):
        return reverse('TedadSathShabake')


class SodeModirView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Sode_Modir.html'
    form_class = SodeModirForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='sode_modir', defaults={
            "onvan": 'sode_modir',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(SodeModirView, self).form_valid(form)

    def get_success_url(self):
        return reverse('SodeModir')


class Languge_siteView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Languge_site.html'
    form_class = Languge_siteForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='languge_site', defaults={
            "onvan": 'languge_site',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(Languge_siteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Languge_site')


class Count_Level_networkView(LoginRequiredMixin, CreateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Count_level_network.html'
    form_class = Count_level_networkForm


    def form_valid(self, form):
        Count_Level_network = form.save(commit=False)

        messages.success(self.request, 'سطح موردنظر ثبت شد')
        return super(Count_Level_networkView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Count_Level_networkView')


class Count_Level_networkDataTableView(LoginRequiredMixin, BaseDatatableView):
    model =TanzimatPaye
    columns = ['id','onvan','value']
    order_columns = ['id','onvan','value']
    # max_display_length = 1

    def get_initial_queryset(self):
        qs = super().get_initial_queryset()
        qs = qs.filter(onvan__startswith='سطح')
        return qs

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(onvan__icontains=search)
        return qs

class Count_Level_networkDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        # if request.user.is_administrator:

        Count_Level_network = get_object_or_404(TanzimatPaye, pk=pk)
        print("count_level_network",Count_Level_network)

        Count_Level_network.delete()

        messages.success(self.request, 'سطح موردنظر با موفقیت حذف شد')
        return redirect('Count_Level_networkView')


class Count_Level_networkUpdateView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Update_count_levelnetwork.html'
    form_class = Count_level_networkForm

    def form_valid(self, form):
        count_level_network = form.save(commit=False)

        messages.success(self.request, 'سطح مورد نظر ویرایش شد.')
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
#         messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
#         return super(Count_Level_networkView, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse('Count_Level_networkView')

class Count_kharid_hadaghalView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Count_kharid_hadaghal.html'
    form_class = Count_kharid_hadaghalForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='count_kharid_hadaghl', defaults={
            "onvan": 'count_kharid_hadaghl',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
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
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
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
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(Taien_meghdar_matlabView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Taien_meghdar_matlabView')


class Show_amar_foruserView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Show_amar_foruser.html'
    form_class = Show_amarforuserForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='show_amar_for_user', defaults={
            "onvan": 'show_amar_for_user',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
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
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(Taeid_khodkar_tablighView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Taeid_khodkar_tabligh')

class Vahed_poll_siteView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Vahed_poll_site.html'
    form_class = Vahed_poll_siteForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='vahed_poll_site', defaults={
            "onvan": 'vahed_poll_site',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(Vahed_poll_siteView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Vahed_poll_site')




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
            messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
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
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(Taein_hadaghal_etbarView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Taein_hadaghal_etbar')

class Amar_jaali_View(LoginRequiredMixin,View):
    # model = TanzimatPaye
    # template_name = 'system/TanzimatPaye/Amar_jaali.html'
    # form_class = Amar_jaali_Form

    def post(self,request):
        count_user_online=self.request.POST.get('count_user_online')
        count_all_user=self.request.POST.get('count_all_user')
        count_user_new_today=self.request.POST.get('count_user_new_today')
        meghdar_daramad_pardahkti=self.request.POST.get('meghdar_daramad_pardahkti')
        count_tabligh_thabti=self.request.POST.get('count_tabligh_thabti')
        print("count_all_user",count_all_user)
        print("count_user_new_today",count_user_new_today)
        print("meghdar_daramad_pardahkti",meghdar_daramad_pardahkti)

        amar_jaali=TanzimatPaye.objects.filter(onvan__startswith='amar_jaali').all()
        print("amar_jalali",amar_jaali)
        for item in amar_jaali:
            if item.onvan=="amar_jaali.count_user_online":
                item.value=count_user_online
                item.save()
            if item.onvan=="amar_jaali.count_all_user":
                item.value=count_all_user
                item.save()
            if item.onvan=="amar_jaali.count_user_new_today":
                item.value=count_user_new_today
                item.save()
            if item.onvan=="amar_jaali.meghdar_daramad_pardahkti":
                item.value=meghdar_daramad_pardahkti
                item.save()
            if item.onvan=="amar_jaali.count_tabligh_thabti":
                item.value=count_tabligh_thabti
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
        count_user_new_today, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_user_new_today', defaults={
            "onvan": 'amar_jaali.count_user_new_today',
            'value': 0,
        })
        meghdar_daramad_pardahkti, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.meghdar_daramad_pardahkti',
                                                                          defaults={
                                                                              "onvan": 'amar_jaali.meghdar_daramad_pardahkti',
                                                                              'value': 0,
                                                                          })
        count_tabligh_thabti, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_tabligh_thabti', defaults={
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
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')

        return render(request,'system/TanzimatPaye/Amar_jaali.html',{'form':form})



    def get(self, request):

        count_user_online, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_user_online', defaults={
            "onvan": 'amar_jaali.count_user_online',
            'value': 0,
        })

        count_all_user, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_all_user', defaults={
            "onvan": 'amar_jaali.count_all_user',
            'value': 0,
        })
        count_user_new_today, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_user_new_today', defaults={
            "onvan": 'amar_jaali.count_user_new_today',
            'value': 0,
        })
        meghdar_daramad_pardahkti, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.meghdar_daramad_pardahkti', defaults={
            "onvan": 'amar_jaali.meghdar_daramad_pardahkti',
            'value': 0,
        })
        count_tabligh_thabti, _ = TanzimatPaye.objects.get_or_create(onvan='amar_jaali.count_tabligh_thabti', defaults={
            "onvan": 'amar_jaali.count_tabligh_thabti',
            'value': 0,
        })
        form = Amar_jaali_Form(data={
            'count_user_online':count_user_online.value,
            'count_all_user':count_all_user.value,
            'count_user_new_today':count_user_new_today.value,
            'meghdar_daramad_pardahkti':meghdar_daramad_pardahkti.value,
            'count_tabligh_thabti':count_tabligh_thabti.value
        })
        # print("form",form)

        return render(request,'system/TanzimatPaye/Amar_jaali.html',{'form':form})
        # return obj


    def get_success_url(self):
        return reverse('Amar_jaali')




