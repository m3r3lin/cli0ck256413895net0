from django.contrib import messages
from django.urls import reverse
from django.views.generic import UpdateView

from Ads_Project.functions import LoginRequiredMixin
from system.forms import ActiveCodeMoarefForm, SodeModirForm,\
    Languge_siteForm,Count_level_networkForm,Count_kharid_hadaghalForm,Time_kharid_termForm,\
    Taien_meghdar_matlabForm,Show_amarforuserForm,Taied_khodkar_tablighForm

from system.models import TanzimatPaye, ACTIV_MOAREF


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

class Count_Level_networkView(LoginRequiredMixin, UpdateView):
    model = TanzimatPaye
    template_name = 'system/TanzimatPaye/Count_level_network.html'
    form_class = Count_level_networkForm

    def get_object(self, queryset=None):
        obj, cre = TanzimatPaye.objects.get_or_create(onvan='count_level_network', defaults={
            "onvan": 'count_level_network',
            'value': 0,
        })
        return obj

    def form_valid(self, form):
        messages.success(self.request, 'تنظیمات مورد نظر ویرایش شد.')
        return super(Count_Level_networkView, self).form_valid(form)

    def get_success_url(self):
        return reverse('Count_Level_networkView')

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



