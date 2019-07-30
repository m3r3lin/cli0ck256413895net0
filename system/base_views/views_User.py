from django.contrib import auth, messages
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from Ads_Project.functions import LoginRequiredMixin
from system.forms import UserCreateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import logout
from django.urls import reverse

from system.models import User


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
        return reverse('CreateUser')


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

    # def get_object(self, queryset=None):
    #     return self.request.user

    def form_valid(self, form):
        if 'avatar' in self.request.FILES:
            user = User.objects.get(username=self.request.user.username)
            user.avatar = self.request.FILES['avatar']
            print('avatar saveed!!!')
        if 'image_cart_melli' in self.request.FILES:
            user = User.objects.get(username=self.request.user.username)
            user.avatar = self.request.FILES['image_cart_melli']
            print('image_cart_melli saveed!!!')
        messages.success(self.request, 'تغییرات شما یا موفقیت ثبت شد')
        return super(UserUpdateView, self).form_valid(form)

    def get_success_url(self):
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
