from builtins import object

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
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
        history=History.objects.create(user=user,type='0',meghdar=int(form.cleaned_data['how_much']))

        return super(IncreaseBalanceView, self).form_valid(form)
        # TODO what should we do with other orders ?
        order = Order.objects.create(user_id=user_id, type=INCREASE_BALANCE_ORDER, data=dict(
            mount=form.cleaned_data['how_much']
        ))
        url = 'http://127.0.0.1:8000/system/increase_balance/'
        return redirect(f'/system/virtual_bank_verification1/?order_id={order.id}&redirect')

    def form_invalid(self, form):
        return super().form_invalid(form)
