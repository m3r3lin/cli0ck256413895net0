from builtins import object
from typing import re

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django_datatables_view.base_datatable_view import BaseDatatableView
from system.templatetags.app_filters import date_jalali
from Ads_Project.functions import LoginRequiredMixin
from system.forms import IncreaseBalanceFrom
from system.models import Order, User, INCREASE_BALANCE_ORDER , History


def dargah_test_part_1(request):
    a = f"""
    <a href=\"{request.GET.get('redirect')}?password=150&username=husseinmirzaki&order_id={request.GET.get('order_id')}&\">next</a>
    """
    return HttpResponse(a)


def dargah_test_part_2(request):
    pass


def dargah_test_part_2(request):
    pass


class IncreaseBalanceView(LoginRequiredMixin, FormView):
    template_name = 'system/Malli/Increase_Balance.html'
    form_class = IncreaseBalanceFrom
    success_url = reverse_lazy('increase_balance')

    def get(self, request, *args, **kwargs):
        if request.GET.get('balance_increased'):
            messages.success(request, 'اعتبار شما افزایش پیدا کرد')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user_id = self.request.POST.get('user', None)
        if user_id and (isinstance(user_id, int) or (isinstance(user_id, str) and user_id.isdigit())):
            user_id = int(user_id)
            if User.objects.filter(pk=user_id).exists():
                messages.error(self.request, 'کاربر مورد نظر شما برای افزایش اعتبار موجود نمی باشد')
                return super().form_invalid(form)

        else:
            user_id = self.request.user.id
        user = get_object_or_404(User,pk=int(user_id))
        user.add_to_kif_pool(form.cleaned_data['how_much'])
        History.objects.create(user=user,type='0',meghdar=int(form.cleaned_data['how_much']))

        return super(IncreaseBalanceView, self).form_valid(form)
        # TODO what should we do with other orders ?
        order = Order.objects.create(user_id=user_id, type=INCREASE_BALANCE_ORDER, data=dict(
            mount=form.cleaned_data['how_much']
        ))
        url = 'http://127.0.0.1:8000/system/increase_balance/'
        return redirect(f'/system/virtual_bank_verification1/?order_id={order.id}&redirect')

    def form_invalid(self, form):
        return super().form_invalid(form)




class HistoryMaliListView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'system/Malli/List_malihistory.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class HistoryMaliDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = History
    columns = ['id', 'user', 'type','meghdar','created_at' ]

    def get_initial_queryset(self):
        user=self.request.user
        qs = super().get_initial_queryset()
        if user.is_superuser:
            return qs
        qs = qs.filter(user=user)
        return qs

    def render_column(self, row, column):
        if column == 'created_at':
            return date_jalali(row.created_at,3)
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if self.request.user.is_superuser:
            if search:
                if search in "واریز":
                    qs = qs.filter(Q(type=0) | Q(meghdar__icontains=search) | Q(user__username__icontains=search))
                elif search in "برداشت":
                    qs = qs.filter(Q(type=1) | Q(meghdar__icontains=search  | Q(user__username__icontains=search)))
                elif search in "انتقال از کیف درآمد به کیف پول":
                    qs = qs.filter(Q(type=2) | Q(meghdar__icontains=search) | Q(user__username__icontains=search))
                else:
                    qs = qs.filter(Q(meghdar__icontains=search) | Q(user__username__icontains=search))
        else:
            if search:
                if search in "واریز":
                    qs = qs.filter(Q(type=0) | Q(meghdar__icontains=search))
                elif search in "برداشت":
                    qs = qs.filter(Q(type=1) | Q(meghdar__icontains=search))
                elif search in "انتقال از کیف درآمد به کیف پول":
                    qs = qs.filter(Q(type=2) | Q(meghdar__icontains=search))
                else:
                    qs = qs.filter(Q(meghdar__icontains=search))
        return qs


class MoveDaramad2KifView(LoginRequiredMixin, FormView):
    template_name = 'system/Malli/move_daramad_kif.html'
    form_class = IncreaseBalanceFrom
    success_url = reverse_lazy('MoveDaramad2Kif')

    def get(self, request, *args, **kwargs):
        if request.GET.get('balance_increased'):
            messages.success(request, 'اعتبار شما افزایش پیدا کرد')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = get_object_or_404(User,pk=int(self.request.user.id))
        get_value=int(form.cleaned_data['how_much'])
        kif_daramad=user.get_kif_daramad()
        if (kif_daramad.current_recieved_direct + kif_daramad.current_recieved_indirect)>=get_value:
            if kif_daramad.current_recieved_indirect < kif_daramad.current_recieved_direct :
                if get_value >= kif_daramad.current_recieved_indirect:
                    get_value-=kif_daramad.current_recieved_indirect
                    kif_daramad.current_recieved_indirect=0
                    if get_value>0:
                        kif_daramad.current_recieved_direct-=get_value
                    kif_daramad.save()
                else:
                    kif_daramad.daramad.current_recieved_indirect-=get_value
                    kif_daramad.save()
            else:
                if get_value >= kif_daramad.daramad.current_recieved_direct:
                    get_value -= kif_daramad.current_recieved_direct
                    kif_daramad.current_recieved_direct = 0
                    if get_value > 0:
                        kif_daramad.current_recieved_indirect -= get_value
                        kif_daramad.save()
                else:
                    kif_daramad.daramad.current_recieved_direct-=get_value
                    kif_daramad.save()
            get_value = int(form.cleaned_data['how_much'])
            kif_pol=user.get_kif_kif_pool()
            kif_pol.current_balance+=int(get_value)
            kif_pol.save()
            History.objects.create(user=user, type='2', meghdar=int(form.cleaned_data['how_much']))
            messages.success(self.request, 'مبلغ درخواستی شما با موفقیت به کیف پول منتقل شد.')
            return super(MoveDaramad2KifView, self).form_valid(form)
        else:
            messages.error(self.request, 'مقدار وارد شده ار درآمد کسب شده بیشتر میباشد.')
            return super(MoveDaramad2KifView, self).form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


