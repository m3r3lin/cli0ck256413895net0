from itertools import groupby
from django.forms import ModelForm, FileInput, Form
from django import forms
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import json
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django_datatables_view.base_datatable_view import BaseDatatableView
from operator import itemgetter
from Ads_Project.functions import LoginRequiredMixin
from django.views.generic import CreateView, ListView, FormView, View, UpdateView
from django.views.generic import TemplateView
from django.http import HttpResponse
from system.models import User, BannerSingup
from system.forms import NewMessageCreateForm, CreateTicketForm, Create_Banner
from django.db.models import Q
from django.contrib import messages
from django.db.models import ProtectedError


class BannerCreateView(LoginRequiredMixin, CreateView):
    model = BannerSingup
    template_name = 'system/BannerSignup/Create_Banner.html'
    form_class = Create_Banner

    def form_valid(self, form):
        messages.success(self.request, "بنر با موفقیت ایجاد شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('Create_Banner')


class BannerListView(LoginRequiredMixin, TemplateView):
    template_name = 'system/BannerSignup/List_Banner.html'


class BannerDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = BannerSingup
    columns = ['id', 'pic', 'description', 'size']

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(description__icontains=search) | Q(size__icontains=search))
        return qs


class BannerUpdateView(LoginRequiredMixin, UpdateView):
    model = BannerSingup
    template_name = 'system/BannerSignup/Create_Banner.html'
    form_class = Create_Banner

    def form_valid(self, form):
        messages.success(self.request, "بنر با موفقیت ویرایش شد.")
        return super(BannerUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('List_Banner')


class BannerDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            pelan = get_object_or_404(BannerSingup, pk=pk)
            pelan.delete()
        except ProtectedError:
            messages.error(self.request, "متاسفانه بنر حذف نشد")
            return redirect('List_Banner')
        messages.success(self.request, "بنر با موفقیت حذف شد")
        return redirect('List_Banner')


class List_Banner_show_View(LoginRequiredMixin, ListView):
    model = BannerSingup
    template_name = 'system/BannerSignup/List_Show_Banner.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context
