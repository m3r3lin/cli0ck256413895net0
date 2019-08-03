from django.contrib import messages
from django.urls import reverse
from django.views.generic import UpdateView

from Ads_Project.functions import LoginRequiredMixin
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
