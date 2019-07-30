from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from Ads_Project.functions import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView

from system.forms import PelanCreateForm
from system.models import Pelan


class PelanCreateView(LoginRequiredMixin, CreateView):
    template_name = 'system/Pelan/create_pelan.html'
    form_class = PelanCreateForm

    def form_valid(self, form):
        user = form.save(commit=False)
        messages.success(self.request, 'پلن مورد نظر با موفقیت ثبت شد.')
        return super(PelanCreateView, self).form_valid(form)

    def form_invalid(self, form):
        print(self.request.POST)
        return super(PelanCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('CreatePelan')


class PelanUpdateView(LoginRequiredMixin, UpdateView):
    model = Pelan
    template_name = 'system/Pelan/update_pelan.html'
    form_class = PelanCreateForm

    def form_valid(self, form):
        pelan = form.save(commit=False)
        messages.success(self.request, 'پلن مورد نظر ویرایش شد.')
        return super(PelanUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ListPelan')


class PelanDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            pelan = get_object_or_404(Pelan, pk=pk)
            pelan.delete()
        except ProtectedError:
            messages.error(self.request, 'از این نوع پلن قبلا استفاده شده است و قابل حذف نمیباشد.')
            return redirect('ListPelan')
        messages.success(self.request, 'پلن موردنظر با موفقیت حذف شد')
        return redirect('ListPelan')


class PelanListView(LoginRequiredMixin, ListView):
    model = Pelan
    template_name = 'system/Pelan/list_pelan.html'
    form_class = PelanCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        # context = super().get_context_data(object_list=Pelan.objects.order_by('-onvan'), **kwargs)
        return context
