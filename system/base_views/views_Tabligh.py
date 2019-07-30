from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import ProtectedError
from django.http import request
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView

from system.forms import TablighCreateForm
from system.models import Tabligh
from system.templatetags.app_filters import date_jalali


class TablighCreateView(LoginRequiredMixin, CreateView):
    template_name = 'system/Tabligh/Create_Tabligh.html'
    form_class = TablighCreateForm

    def form_valid(self, form):
        tabligh = form.save(commit=False)
        messages.success(self.request, 'تبلیغ مورد نظر با موفقیت ثبت شد.')
        return super(TablighCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(self.request.POST)
        return super(TablighCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('ListTabligh')


class TablighUpdateView(LoginRequiredMixin, UpdateView):
    model = Tabligh
    template_name = 'system/Tabligh/Update_Tabligh.html'
    form_class = TablighCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        # tabligh = form.save(commit=False)
        messages.success(self.request, 'تبلیغ مورد نظر ویرایش شد.')
        return super(TablighUpdateView, self).form_valid(form)

    def get_success_url(self):
        # return reverse('UpdateTabligh', kwargs={'pk': self.object.pk})
        return reverse('ListTabligh')


class TablighDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            tabligh = get_object_or_404(Tabligh, pk=pk)
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
    columns = ['id', 'onvan', 'code_tabligh_gozaar', 'tarikh_ijad', 'code_pelan', 'tedad_click', 'tedad_click_shode', 'link', 'vazeyat']

    def render_column(self, row, column):
        if column == 'tarikh_ijad':
            return date_jalali(row.tarikh_ijad)
        return super().render_column(row, column)
