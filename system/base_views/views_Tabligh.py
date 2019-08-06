import random
import random
import string

from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from system.forms import TablighCreateForm
from system.models import Tabligh, TanzimatPaye, TAIED_KHODKAR_TABLIGH, TAIEN_MEGHDAR_MATLAB, Click, TablighatMontasherKonande
from system.templatetags.app_filters import date_jalali


class TablighCreateView(LoginRequiredMixin, CreateView):
    template_name = 'system/Tabligh/Create_Tabligh.html'
    form_class = TablighCreateForm

    @staticmethod
    def random_string(length):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            messages.error(request, 'کاربر ادمین نمیتواند تبلیغ ایجاد کند')
            return redirect(reverse('dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.code_tabligh_gozaar_id = self.request.user.id
        t = form.instance.text.__len__()
        max_t = int(TanzimatPaye.get_settings(TAIEN_MEGHDAR_MATLAB, False))
        if t > max_t:
            messages.error(self.request, 'طول تبلیغ بیش از حد مجاز است')
            return super(TablighCreateView, self).form_invalid(form)

        if TanzimatPaye.get_settings(TAIED_KHODKAR_TABLIGH, False) == '1':
            form.instance.vazeyat = 1
        else:
            form.instance.vazeyat = 3
        r = form.instance.code_pelan.gheymat
        kife_pool = self.request.user.get_kif_kif_pool()
        pool = kife_pool.current_balance
        if pool < r:
            messages.error(self.request, 'شما اعتبار کافی ندارید')
            return super(TablighCreateView, self).form_invalid(form)

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
            messages.success(self.request, 'مشکلی در ایجاد تبلیغ شما اتفاق افتاده است لطفاً دوباره تلاش کنید')
            return super(TablighCreateView, self).form_invalid(form)

        messages.success(self.request, 'تبلیغ مورد نظر با موفقیت ثبت شد.')
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
                messages.error(self.request, 'طول تبلیغ بیش از حد مجاز است')
                return super(TablighCreateView, self).form_invalid(form)

            try:
                obj = Tabligh.objects.get(pk=self.object.pk)
            except:
                messages.error(self.request, 'مشکلی پیش آمده با مدیر تماس بگیرید')
                return self.form_invalid(form)
            form.instance.code_tabligh_gozaar_id = self.request.user.id

            if form.instance.onvan != obj.onvan or form.instance.text != obj.text:
                form.instance.vazeyat = 3
            else:
                form.instance.vazeyat = self.object.vazeyat

            form.instance.code_pelan = obj.code_pelan
            form.instance.tedad_click = obj.tedad_click
            form.instance.tedad_click_shode = obj.tedad_click_shode

        messages.success(self.request, 'تبلیغ مورد نظر ویرایش شد.')
        return super(TablighUpdateView, self).form_valid(form)

    def get_success_url(self):
        # return reverse('UpdateTabligh', kwargs={'pk': self.object.pk})
        return reverse('ListTabligh')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields['code_tabligh_gozaar'].required = False
            form.fields['vazeyat'].choices = ((0, 'غیرفعال'), (1, 'فعال'))
            form.fields['code_pelan'].required = False
            form.fields['tedad_click'].required = False
            form.fields['tedad_click_shode'].required = False

        return form


class TablighDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            tabligh = get_object_or_404(Tabligh, pk=pk)
            if tabligh.tedad_click_shode > 0 or Click.objects.filter(tabligh=tabligh).exists():
                messages.error(self.request, 'تبلیغ مورد نظر شما نمی تواند حذف شود شما می توانید این تبلیغ را غیر فعال کنید')
                return redirect('ListTabligh')
            request.user.add_to_kif_pool(tabligh.mablagh_tabligh)
            tabligh.delete()
        except ProtectedError:
            messages.error(self.request, 'از این نوع تبلیغ قبلا استفاده شده است و قابل حذف نمیباشد.')
            return redirect('ListTabligh')
        messages.success(self.request, 'تبلیغ موردنظر با موفقیت حذف شد')
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
    columns = ['id', 'onvan', 'code_tabligh_gozaar', 'tarikh_ijad', 'code_pelan', 'tedad_click', 'tedad_click_shode', 'vazeyat', 'random_url']

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

    def render_column(self, row:TablighatMontasherKonande, column):
        if column == 'tarikh':
            return date_jalali(row.tarikh)
        elif column == 'tabligh':
            return row.tabligh_id
        elif column == 'onvan_tabligh':
            return row.tabligh.onvan
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(onvan__icontains=search) | Q(code_tabligh_gozaar__username__icontains=search))
        if not self.request.user.is_superuser:
            qs = qs.filter(code_tabligh_gozaar=self.request.user)
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
        if request.user.is_superuser:
            messages.error(request, 'ادمین نمیتواند منتشر کننده باشد')
        else:
            tabligh = get_object_or_404(Tabligh, random_url=tabligh_token)
            tabligh_montasher, _ = TablighatMontasherKonande.objects.get_or_create(montasher_konande=request.user, tabligh=tabligh,
                                                                                   defaults={
                                                                                       'montasher_konande': request.user,
                                                                                       'tabligh': tabligh
                                                                                   })
            messages.success(request, 'درخواست شما با موفقیت ثبت شد.')
        if ref == 'dashboard':
            return redirect(reverse('dashboard'))
        else:
            return redirect(reverse('ShowTablighs'))


class PublishShowView(LoginRequiredMixin, TemplateView):
    template_name = 'system/Tabligh/Publish_Tabligh.html'

    def get_context_data(self, **kwargs):
        kwargs['tablighs'] = Tabligh.objects.filter(vazeyat=1).order_by('-id')[:10]
        return super().get_context_data(**kwargs)


class ShowTablighView(TemplateView):
    template_name = 'system/Tabligh/Show_Tabligh.html'
