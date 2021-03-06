import random
import string

from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from system.forms import TablighCreateForm
from system.models import (
    Tabligh, TanzimatPaye, TAIED_KHODKAR_TABLIGH, TAIEN_MEGHDAR_MATLAB, Click,
    TablighatMontasherKonande, SATH, SoodeTabligh,
    COUNT_LEVEL_NETWORK, SODE_MODIR, User, LEAST_BALANCE_REQUIRED, CLICK_IS_CHANGEABLE
)
from system.templatetags.app_filters import date_jalali


class TablighCreateView(LoginRequiredMixin, CreateView):
    template_name = 'system/Tabligh/Create_Tabligh.html'
    form_class = TablighCreateForm

    @staticmethod
    def random_string(length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            messages.error(request, _("Admin can't create Ad"))
            return redirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.code_tabligh_gozaar_id = self.request.user.id
        t = form.instance.text.__len__()

        max_t = int(TanzimatPaye.get_settings(TAIEN_MEGHDAR_MATLAB, False))
        if t > max_t:
            messages.error(self.request, _("Ad text is too long"))
            return super(TablighCreateView, self).form_invalid(form)

        if TanzimatPaye.get_settings(TAIED_KHODKAR_TABLIGH, False) == '1':
            form.instance.vazeyat = 1
        else:
            form.instance.vazeyat = 3
        r = form.instance.code_pelan.gheymat
        kife_pool = self.request.user.get_kif_kif_pool()
        pool = kife_pool.current_balance
        if pool < r:
            messages.error(self.request, _("Your balance is too low"))
            return super(TablighCreateView, self).form_invalid(form)

        if not TanzimatPaye.get_settings(CLICK_IS_CHANGEABLE, 0):
            form.instance.mablagh_har_click = form.instance.code_pelan.gheymat / form.instance.code_pelan.tedad_click
            form.instance.tedad_click = form.instance.code_pelan.tedad_click
        else:
            form.instance.mablagh_har_click = form.instance.code_pelan.gheymat / form.instance.tedad_click

        form.instance.mablagh_tabligh = form.instance.code_pelan.gheymat

        random_string = list(self.random_string(12) + str(self.request.user.id))
        random.shuffle(random_string)
        random.shuffle(random_string)
        form.instance.random_url = ''.join(random_string)

        form = super(TablighCreateView, self).form_valid(form)
        try:
            kife_pool.current_balance = pool - r
            kife_pool.save()
        except Exception as e:
            # todo make sure balance is reduced
            print(e)
            messages.error(self.request, _("While creating the Ad some problem occurred"))
            return super(TablighCreateView, self).form_invalid(form)
        tedad_sath_shabake = TanzimatPaye.get_settings(COUNT_LEVEL_NETWORK, 0)
        sode_modir = TanzimatPaye.get_settings(SODE_MODIR, 0)

        soode_admin_kol = ((self.object.mablagh_tabligh * sode_modir) / 100)
        soode_admin = ((self.object.mablagh_har_click * sode_modir) / 100)
        pool_ezafe = self.object.mablagh_har_click - soode_admin
        User.objects.filter(is_superuser=True).first().add_to_kif_pool(soode_admin_kol)
        SoodeTabligh.objects.get_or_create(sath=0, tabligh=self.object, defaults={
            "sath": 0,
            "tabligh": self.object,
            "soode_mostaghim": soode_admin_kol,
            "soode_gheire_mostaghim": 0,
        })

        if tedad_sath_shabake == 0:
            SoodeTabligh.objects.get_or_create(sath=1, tabligh=self.object, defaults={
                "sath": 1,
                "tabligh": self.object,
                "soode_mostaghim": pool_ezafe,
                "soode_gheire_mostaghim": 0,
            })
        else:
            sum = 0
            for i in range(tedad_sath_shabake):
                sath = i + 1
                settings_sood = TanzimatPaye.get_settings(SATH + str(sath), 0)

                if settings_sood == 0:
                    sood = 0
                else:
                    sood = (pool_ezafe * settings_sood) / 100

                if settings_sood + sum == 0:
                    sood_gheir_mostaghim = 0
                else:
                    sood_gheir_mostaghim = (pool_ezafe * (settings_sood + sum)) / 100

                SoodeTabligh.objects.get_or_create(sath=sath, tabligh=self.object, defaults={
                    "sath": sath,
                    "tabligh": self.object,
                    "soode_mostaghim": pool_ezafe - sood_gheir_mostaghim,
                    "soode_gheire_mostaghim": sood,
                })
                sum += settings_sood

        messages.success(self.request, _("Your Ad is created"))
        return form

    def form_invalid(self, form):
        print(self.request.POST)
        return super(TablighCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('ListTabligh')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['code_tabligh_gozaar'].required = False
        if not TanzimatPaye.get_settings(CLICK_IS_CHANGEABLE, 0):
            del form.fields['tedad_click']
        return form


class TablighUpdateView(LoginRequiredMixin, UpdateView):
    model = Tabligh
    template_name = 'system/Tabligh/Update_Tabligh.html'
    form_class = TablighCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            t = form.instance.text.__len__()
            max_t = int(TanzimatPaye.get_settings(TAIEN_MEGHDAR_MATLAB, False))
            if t > max_t:
                messages.error(self.request, _("Ad text is too long"))
                return super(TablighCreateView, self).form_invalid(form)

            try:
                obj = Tabligh.objects.get(pk=self.object.pk)
            except:
                messages.error(self.request, _("While updating the Ad some problem occurred"))
                return self.form_invalid(form)
            form.instance.code_tabligh_gozaar_id = self.request.user.id

            if form.instance.onvan != obj.onvan or form.instance.text != obj.text:
                form.instance.vazeyat = 3
            else:
                form.instance.vazeyat = self.object.vazeyat

            form.instance.code_pelan = obj.code_pelan
            form.instance.tedad_click = obj.tedad_click
            form.instance.tedad_click_shode = obj.tedad_click_shode

        messages.success(self.request, _("Your Ad is updated"))
        return super(TablighUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ListTabligh')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['code_tabligh_gozaar'].required = False
            form.fields['vazeyat'].choices = ((0, _("activate")), (1, _("deactivate")))
            form.fields['code_pelan'].required = False
            form.fields['tedad_click'].required = False
            form.fields['tedad_click_shode'].required = False

        return form


class TablighDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            tabligh = get_object_or_404(Tabligh, pk=pk)
            if tabligh.tedad_click_shode > 0 or Click.objects.filter(tabligh=tabligh).exists():
                messages.error(self.request, _("This Ad can't be deleted you can disable it"))
                return redirect('ListTabligh')
            tabligh.code_tabligh_gozaar.add_to_kif_pool(tabligh.mablagh_tabligh)
            SoodeTabligh.objects.filter(sath=0, tabligh=tabligh)
            first_soode_tabligh = SoodeTabligh.objects.filter(sath=0, tabligh=tabligh).first()
            User.objects.filter(is_superuser=True).first().sub_from_kif_pool(
                first_soode_tabligh.soode_mostaghim if first_soode_tabligh else 0)
            tabligh.delete()
        except ProtectedError:
            messages.error(self.request, _("This Ad can't be deleted you can disable it"))
            return redirect('ListTabligh')
        messages.success(self.request, _("Ad is deleted successfully and the balance is ba to your account"))
        return redirect('ListTabligh')


class TablighListView(LoginRequiredMixin, ListView):
    model = Tabligh
    template_name = 'system/Tabligh/List_Tabligh.html'
    form_class = TablighCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class TablighDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = Tabligh
    columns = ['id', 'onvan', 'code_tabligh_gozaar', 'tarikh_ijad', 'code_pelan', 'tedad_click', 'tedad_click_shode',
               'vazeyat', 'random_url']

    def render_column(self, row, column):
        if column == 'tarikh_ijad':
            return date_jalali(row.tarikh_ijad)
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(onvan__icontains=search) | Q(code_tabligh_gozaar__username__icontains=search))
        if not self.request.user.is_superuser:
            qs = qs.filter(code_tabligh_gozaar=self.request.user)
        return qs


class MotashershodeDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = TablighatMontasherKonande
    columns = ['id', 'tabligh_id', 'montasher_konande', 'onvan_tabligh', 'tarikh', 'pelan',
               'tedad_click', 'tedad_click_shode', 'vazeyat', 'random_url']

    def render_column(self, row: TablighatMontasherKonande, column):
        if column == 'tarikh':
            return date_jalali(row.tarikh)
        elif column == 'tabligh':
            return row.tabligh_id
        elif column == 'onvan_tabligh':
            return row.tabligh.onvan
        elif column == 'pelan':
            return row.tabligh.code_pelan.onvan
        elif column == 'tedad_click':
            return row.tabligh.tedad_click
        elif column == 'tedad_click_shode':
            return row.tabligh.tedad_click_shode
        elif column == 'vazeyat':
            return row.tabligh.vazeyat
        elif column == 'random_url':
            return row.tabligh.random_url
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(onvan__icontains=search) | Q(code_tabligh_gozaar__username__icontains=search))
        return qs


class TablighPreviewView(LoginRequiredMixin, View):
    def get(self, request, tabligh_token):
        tabligh = get_object_or_404(Tabligh, random_url=tabligh_token)
        return render(request, 'system/Tabligh/Show_Tabligh.html', context={
            'tabligh': tabligh
        })


class PublishTablighView(LoginRequiredMixin, View):

    def get(self, request, tabligh_token):
        ref = request.GET.get('ref', None)
        self.least_balance = None

        def get_least_balance():
            if self.least_balance is None:
                self.least_balance = TanzimatPaye.get_settings(LEAST_BALANCE_REQUIRED, 0)
            return self.least_balance

        if request.user.is_superuser:
            messages.error(request, _("Admin can't be a publisher"))
            return redirect(reverse('dashboard'))
        elif request.user.get_kif_kif_pool().current_balance < get_least_balance():
            messages.error(request, _("Least balance required to add or see Ads is {}").format(get_least_balance()))
            return redirect(reverse('dashboard'))
        else:
            tabligh = get_object_or_404(Tabligh, random_url=tabligh_token)
            tabligh_montasher, d = TablighatMontasherKonande.objects.get_or_create(montasher_konande=request.user,
                                                                                   tabligh=tabligh,
                                                                                   defaults={
                                                                                       'montasher_konande': request.user,
                                                                                       'tabligh': tabligh
                                                                                   })
            messages.success(request, _("You have published one Ad"))
        if ref == 'dashboard':
            return redirect(reverse('dashboard'))
        else:
            return redirect(reverse('ShowTablighs'))


class PublishShowView(LoginRequiredMixin, TemplateView):
    template_name = 'system/Tabligh/Publish_Tabligh.html'

    def get_context_data(self, **kwargs):
        kwargs['tablighs'] = Tabligh.objects.filter(vazeyat=1).order_by('-id')[:10]
        return super().get_context_data(**kwargs)


class Montashshodeha(LoginRequiredMixin, TemplateView):
    template_name = 'system/Tabligh/List_Enteshar.html'


class ShowTablighView(TemplateView):
    template_name = 'system/Tabligh/Show_Tabligh.html'


class ActivateTablighView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_superuser:
            messages.error(request, _("Your not allowed here"))
            return redirect(reverse('ListTabligh'))
        try:
            tabligh = int(request.GET.get('tabligh'))
        except:
            messages.error(request, _("Wrong input"))
            return redirect(reverse('ListTabligh'))

        if not tabligh:
            messages.error(request, _("Wrong input"))
            return redirect(reverse('ListTabligh'))
        try:
            tabligh = Tabligh.objects.get(pk=tabligh)
        except:
            messages.error(request, _("Wrong input"))
            return redirect(reverse('ListTabligh'))
        if tabligh.vazeyat == 1:
            tabligh.vazeyat = 0
        else:
            tabligh.vazeyat = 1
        tabligh.save()
        messages.success(request, _("You have published one Ad"))
        return redirect(reverse('ListTabligh'))
