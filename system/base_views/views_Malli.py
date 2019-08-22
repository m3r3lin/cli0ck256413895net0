from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView,View,TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from django import forms
from django.forms import Form, CharField
from Ads_Project.functions import LoginRequiredMixin
from system.forms import IncreaseBalanceFrom
from system.models import Order, User, INCREASE_BALANCE_ORDER, History, Tabligh, COUNT_KHARI_HADAGHAL, TanzimatPaye ,PERFECT_USER_ID,PERFECT_TITLE,PERFECT_PASSPHRASE
from system.templatetags.app_filters import date_jalali
import hashlib
from datetime import datetime


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
    success_url = reverse_lazy('ConfirmBalanceView')

    def get(self, request, *args, **kwargs):
        if request.GET.get('balance_increased'):
            messages.success(request, _("Your balance increased"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        dargah_type = form.cleaned_data['dargah_type']
        how_much = form.cleaned_data['how_much']
        self.request.session['dargah_type'] = dargah_type
        self.request.session['how_much'] = how_much
        my_str=str(self.request.user.id)+' '+self.request.user.username+' '+ str(datetime.now())
        payment_id=hashlib.sha1(my_str.encode("UTF-8")).hexdigest()
        self.request.session['payment_id'] = payment_id
        Order.objects.create(type=INCREASE_BALANCE_ORDER,user=self.request.user,mablagh=float(how_much),payment_id=payment_id,status=0)
        '''user_id = self.request.POST.get('user', None)
        if user_id and (isinstance(user_id, int) or (isinstance(user_id, str) and user_id.isdigit())):
            user_id = int(user_id)
            if User.objects.filter(pk=user_id).exists():
                messages.error(self.request, _("User does not exist"))
                return super().form_invalid(form)

        else:
            user_id = self.request.user.id
        user = get_object_or_404(User, pk=int(user_id))
        user.add_to_kif_pool(form.cleaned_data['how_much'])
        History.objects.create(user=user, type='0', meghdar=int(form.cleaned_data['how_much']))'''

        return super(IncreaseBalanceView, self).form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ConfirmBalanceView(LoginRequiredMixin, TemplateView):
    template_name = 'system/Malli/Confirmation_method.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        if self.request.session.get('dargah_type')=='1':
            form = Form()
            form.fields = {}
            action_url="https://perfectmoney.is/api/step1.asp"
            how_much=self.request.session.get("how_much")
            submit_name="PAYMENT_METHOD"
            dargah_type="Perfect Money"
            PERFECT_USER_ID_VALUE=TanzimatPaye.get_settings(PERFECT_USER_ID,0)
            PUI = forms.CharField(initial=PERFECT_USER_ID_VALUE, widget=forms.HiddenInput())
            form.fields["PAYEE_ACCOUNT"] = PUI
            PAYMENT_ID = forms.CharField(initial=self.request.session.get('payment_id'), widget=forms.HiddenInput())
            form.fields["PAYMENT_ID"] = PAYMENT_ID
            PERFECT_TITLE_VALUE=TanzimatPaye.get_settings(PERFECT_TITLE,0)
            PT = forms.CharField(initial=PERFECT_TITLE_VALUE, widget=forms.HiddenInput())
            form.fields["PAYEE_NAME"] = PT
            PAYMENT_AMOUNT = forms.CharField(initial=self.request.session.get("how_much"), widget=forms.HiddenInput())
            form.fields["PAYMENT_AMOUNT"] = PAYMENT_AMOUNT
            PAYMENT_UNITS = forms.CharField(initial="USD", widget=forms.HiddenInput())
            form.fields["PAYMENT_UNITS"] = PAYMENT_UNITS
            STATUS_URL = forms.CharField(initial="http://9ed79c3b.ngrok.io/system/perfectpaymentstatus", widget=forms.HiddenInput())
            form.fields["STATUS_URL"] = STATUS_URL
            PAYMENT_URL = forms.CharField(initial="http://9ed79c3b.ngrok.io/system/perfectpaymentsuccess", widget=forms.HiddenInput())
            form.fields["PAYMENT_URL"] = PAYMENT_URL
            PAYMENT_URL_METHOD = forms.CharField(initial="GET", widget=forms.HiddenInput())
            form.fields["PAYMENT_URL_METHOD"] = PAYMENT_URL_METHOD
            NOPAYMENT_URL = forms.CharField(initial="http://9ed79c3b.ngrok.io/system/perfect_money_F", widget=forms.HiddenInput())
            form.fields["NOPAYMENT_URL"] = NOPAYMENT_URL
            NOPAYMENT_URL_METHOD = forms.CharField(initial="GET", widget=forms.HiddenInput())
            form.fields["NOPAYMENT_URL_METHOD"] = NOPAYMENT_URL_METHOD
            context["form"]=form
            context["action_url"]=action_url
            context["how_much"]=how_much
            context["submit_name"]=submit_name
            context["dargah_type"]=dargah_type
        return context

    def get(self, request, *args, **kwargs):
        if "payment_id" in request.session:
            return super().get(request, *args, **kwargs)
        else:
            messages.error(request, "فاکتور دریافتی اشتباه است.")
            return redirect(reverse_lazy('increase_balance'))

class PerfectMoneyFailed(View):
    def get(self, request, *args, **kwargs):
        if "payment_id" in request.session:
            print(request.session.get('payment_id'))
            print(request.GET)
            del request.session['payment_id']
            messages.error(request, "پرداخت شما موفقیت آمیز نبود.")
        else:
            messages.error(request, "فاکتور دریافتی اشتباه است.")

        return redirect(reverse_lazy('increase_balance'))

class HistoryMaliListView(LoginRequiredMixin, ListView):
    model = History
    template_name = 'system/Malli/List_malihistory.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class HistoryMaliDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = History
    columns = ['id', 'user', 'type', 'meghdar', 'created_at']

    def get_initial_queryset(self):
        user = self.request.user
        qs = super().get_initial_queryset()
        if user.is_superuser:
            return qs
        qs = qs.filter(user=user)
        return qs

    def render_column(self, row, column):
        if column == 'created_at':
            return date_jalali(row.created_at, 3)
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if self.request.user.is_superuser:
            if search:
                if search in _("deposit"):
                    qs = qs.filter(Q(type=0) | Q(meghdar__icontains=search) | Q(user__username__icontains=search))
                elif search in _("withdraw"):
                    qs = qs.filter(Q(type=1) | Q(meghdar__icontains=search | Q(user__username__icontains=search)))
                elif search in _("Transfer from income money to pocket money"):
                    qs = qs.filter(Q(type=2) | Q(meghdar__icontains=search) | Q(user__username__icontains=search))
                else:
                    qs = qs.filter(Q(meghdar__icontains=search) | Q(user__username__icontains=search))
        else:
            if search:
                if search in _("deposit"):
                    qs = qs.filter(Q(type=0) | Q(meghdar__icontains=search))
                elif search in _("withdraw"):
                    qs = qs.filter(Q(type=1) | Q(meghdar__icontains=search))
                elif search in _("Transfer from income money to pocket money"):
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
            messages.success(request, _("Your balance increased"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        get_value = int(form.cleaned_data['how_much'])

        indirect_allowed = user.allow_indirect()

        kif_daramad = user.get_kif_daramad()
        if (kif_daramad.current_recieved_direct + kif_daramad.current_recieved_indirect) >= get_value:
            if kif_daramad.current_recieved_indirect < kif_daramad.current_recieved_direct:
                if get_value >= kif_daramad.current_recieved_indirect:
                    get_value -= kif_daramad.current_recieved_indirect
                    kif_daramad.current_recieved_indirect = 0
                    if get_value > 0:
                        kif_daramad.current_recieved_direct -= get_value
                    kif_daramad.save()
                else:
                    kif_daramad.current_recieved_indirect -= get_value
                    kif_daramad.save()
            elif indirect_allowed:
                if get_value >= kif_daramad.current_recieved_direct:
                    get_value -= kif_daramad.current_recieved_direct
                    kif_daramad.current_recieved_direct = 0
                    if get_value > 0:
                        kif_daramad.current_recieved_indirect -= get_value
                    kif_daramad.save()
                else:
                    kif_daramad.current_recieved_direct -= get_value
                    kif_daramad.save()

            else:
                if get_value > kif_daramad.current_recieved_direct:
                    messages.error(self.request, _("Selected mount exceeds the withdrawable mount"))
                    return super(MoveDaramad2KifView, self).form_invalid(form)
                else:
                    kif_daramad.current_recieved_direct -= get_value
                    kif_daramad.save()
            get_value = int(form.cleaned_data['how_much'])
            kif_pol = user.get_kif_kif_pool()
            kif_pol.current_balance += int(get_value)
            kif_pol.save()
            History.objects.create(user=user, type='2', meghdar=int(form.cleaned_data['how_much']))
            messages.success(self.request, _("Selected mount is moved to your pocket money"))
            return super(MoveDaramad2KifView, self).form_valid(form)
        else:
            messages.error(self.request, _("Selected mount exceeds the withdrawable mount"))
            return super(MoveDaramad2KifView, self).form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

