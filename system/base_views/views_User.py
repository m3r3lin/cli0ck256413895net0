from django.contrib import auth, messages
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from system.forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import logout
from django.urls import reverse

from system.models import User
from system.templatetags.app_filters import date_jalali


class UserCreateView(CreateView):
    template_name = 'system/user/Create_User.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        accept = self.request.POST.get("accept", False)
        if not accept or accept == 'on':
            if not accept:
                messages.error(self.request, 'لطفاْ قوانین را قبول کنید')
                return super(UserCreateView, self).form_invalid(form)
        else:
            messages.error(self.request, 'مقدار وارد شده برای قوانین اشتباه است')
            return super(UserCreateView, self).form_invalid(form)
        user = form.save(commit=False)
        return super(UserCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('login')


class UserCreateModirView(CreateView):
    template_name = 'system/user/Create_User_Modir.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        return super(UserCreateModirView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserCreateModirView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('ListUser')


def login_user(request):
    if request.user.is_authenticated:
        if request.POST.get('next') is not None:
            return redirect(request.POST.get('next'))
        return redirect('dashboard')
    else:
        if request.method == "POST":
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    if request.GET.get('next') is not None:
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('dashboard')
                else:
                    return render(request, "system/user/login.html", {'error': 'دسترسی شما به سامانه غیر فعال شده است !'})
            else:
                return render(request, "system/user/login.html", {'error': 'نام کاربری یا پسورد شما اشتباه است !'})
        else:
            return render(request, "system/user/login.html")


@login_required
def logout_user(request):
    request.user.last_logout = timezone.now()
    request.user.last_activity = None
    request.user.save()
    logout(request)
    return render(request, "system/user/login.html")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'system/user/Update_User.html'
    form_class = UserUpdateForm

    def form_valid(self, form):
        if 'avatar' in self.request.FILES:
            user = User.objects.get(username=self.request.user.username)
            user.avatar = self.request.FILES['avatar']
        if 'image_cart_melli' in self.request.FILES:
            user = User.objects.get(username=self.request.user.username)
            user.avatar = self.request.FILES['image_cart_melli']

        messages.success(self.request, 'تغییرات شما یا موفقیت ثبت شد')
        return super(UserUpdateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.id != kwargs['pk']:
            messages.error(request, 'شما اجازه دسترسی ندارید')
            return redirect(reverse('UpdateUser', kwargs={'pk': request.user.id}))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        tarikh_tavalod = form.initial['tarikh_tavalod']
        if tarikh_tavalod is not None:
            form.initial['tarikh_tavalod'] = date_jalali(tarikh_tavalod, 3)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.id != kwargs['pk']:
            messages.error(request, 'شما اجازه دسترسی ندارید')
            return redirect(reverse('UpdateUser', kwargs={'pk': request.user.id}))

        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        if not self.request.user.is_superuser:
            return reverse('UpdateUser', kwargs={'pk': self.request.user.id})
        return reverse('ListUser')


class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            user.delete()
        except ProtectedError:
            messages.error(self.request, 'از این نوع کاربر قبلا استفاده شده است و قابل حذف نمیباشد.')
            return redirect('ListUser')
        messages.success(self.request, 'کاربر موردنظر با موفقیت حذف شد')
        return redirect('ListUser')


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'system/user/List_User.html'
    form_class = UserCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        return context


class UserDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = User
    columns = ['id', 'first_name', 'last_name', 'code_melli', 'tarikh_tavalod', 'mobile', 'gender', 'father_name', 'email']

    def render_column(self, row, column):
        if column == 'tarikh_tavalod':
            return date_jalali(row.tarikh_tavalod, 3)
        return super().render_column(row, column)
