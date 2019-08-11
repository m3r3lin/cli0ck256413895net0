from builtins import object

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, CreateView, ListView, UpdateView
from django.views.generic.base import View
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from system.forms import Create_Infopm
from system.models import Infopm


class InfoPm(CreateView):
    template_name = 'system/Infopm/Create_Infopm.html'
    model = Infopm
    form_class = Create_Infopm

    def get_success_url(self):
        messages.success(self.request, 'پیام شما با موفقیت ثبت شد')
        return reverse('Create_InfoPm')


class InfopmUpdateView(LoginRequiredMixin, UpdateView):
    model = Infopm
    template_name = 'system/Infopm/Create_Infopm.html'
    form_class = Create_Infopm

    def form_valid(self, form):
        messages.success(self.request, 'تغییرات شما یا موفقیت ثبت شد')
        return super(InfopmUpdateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(self.request, 'شما اجازه دسترسی ندارید')
            return redirect(reverse('dashboard'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(self.request, 'شما اجازه دسترسی ندارید')
            return redirect(reverse('dashboard'))
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('InpopmrListView')


class InfopmDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        infopm = get_object_or_404(Infopm, pk=pk)
        infopm.delete()
        messages.success(self.request, 'اطلاعیه موردنظر با موفقیت حذف شد')
        return redirect('InpopmrListView')


class InpopmrListView(LoginRequiredMixin, ListView):
    model = Infopm
    template_name = 'system/Infopm/List_Infopm.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context

class InpopmDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = Infopm
    columns = ['id', 'body','is_active' ]

    def render_column(self, row, column):
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(body__icontains=search))
        return qs
