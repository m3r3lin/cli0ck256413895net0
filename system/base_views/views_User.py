from django.contrib import auth, messages
from django.contrib.auth.views import PasswordChangeView
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
from django_datatables_view.base_datatable_view import BaseDatatableView

from Ads_Project.functions import LoginRequiredMixin
from system.forms import UserCreateForm, UserUpdateForm, ChangeUserPasswordForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.models import User
from system.models import User, TanzimatPaye, ACTIV_MOAREF, Parent, TEDAD_SATH_SHABAKE
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
        form.instance.vazeyat = 1
        if TanzimatPaye.get_settings(ACTIV_MOAREF, False) == '1':
            # TODO tanzimat paye check shavad
            id_moaref = form.instance.code_moaref_id
            user = User.objects.get(pk=id_moaref)
            if user.sath + 1 > 10:
                messages.error(self.request, 'تعداد سطوح بیش از مقدار تعیین شده است')
                return super(UserCreateView, self).form_invalid(form)
            form.instance.sath = user.sath + 1
        return super(UserCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserCreateView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('login')


class UserCreateModirView(LoginRequiredMixin, CreateView):
    template_name = 'system/user/Create_User_Modir.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        form.instance.vazeyat = 1
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
        if TanzimatPaye.get_settings(ACTIV_MOAREF, False) == '0' and not self.request.user.is_superuser:
            if form.instance.code_moaref is None or form.instance.code_moaref == '':
                messages.error(self.request, 'کد معرف نمیتواند خالی باید')
                return self.form_invalid(form)

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
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.id != kwargs['pk']:
            messages.error(request, 'شما اجازه دسترسی ندارید')
            return redirect(reverse('UpdateUser', kwargs={'pk': request.user.id}))
        c = super().post(request, *args, **kwargs)

        return c

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        if not self.request.user.is_superuser:
            return reverse('UpdateUser', kwargs={'pk': self.request.user.id})
        return reverse('ListUser')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_superuser:
            form.fields['code_melli'].required = False
            form.fields['gender'].required = False
            form.fields['tarikh_tavalod'].required = False
            form.fields['code_moaref'].required = False
            form.fields['sath'].required = False
            form.fields['image_cart_melli'].required = False
            form.fields['nooe_heshab'].required = False
            form.fields['id_telegram'].required = False
            form.fields['address'].required = False
            form.fields['father_name'].required = False
            form.fields['shomare_hesab'].required = False
            form.fields['shomare_cart'].required = False
            form.fields['shomare_shaba'].required = False
            form.fields['name_saheb_hesab'].required = False
            form.fields['name_bank'].required = False
            form.fields['code_posti'].required = False

        if TanzimatPaye.get_settings(ACTIV_MOAREF, False) == '0' and not self.request.user.is_superuser:
            form.fields['sath'].required = False
        return form


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
    columns = ['id', 'username', 'first_name', 'last_name', 'code_melli', 'tarikh_tavalod', 'mobile', 'gender', 'father_name', 'vazeyat']

    def render_column(self, row, column):
        if column == 'tarikh_tavalod':
            return date_jalali(row.tarikh_tavalod, 3)
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
        return qs


class ChangeUserPasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'system/user/Change_User_Password.html'
    form_class = ChangeUserPasswordForm

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('ChangeUserPassword')


class ProfileUserView(LoginRequiredMixin, View):
    def get(self, request):
        user = User.objects.get(username=request.user.username)
        user.tarikh_tavalod = date_jalali(user.tarikh_tavalod, 3)
        return render(request, 'system/user/Profile_User.html', {'user': user})
