import simplejson as json
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.contrib import auth, messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.db.models import ProtectedError, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from Ads_Project.functions import LoginRequiredMixin
from Ads_Project.settings import MAIN_ADMIN_ID
from system.forms import UserCreateForm, UserUpdateForm, ChangeUserPasswordForm
from system.models import User, TanzimatPaye, ACTIV_MOAREF, COUNT_LEVEL_NETWORK
from system.templatetags.app_filters import date_jalali


class UserCreateView(CreateView):
    template_name = 'system/user/Create_User.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        accept = self.request.POST.get("accept", False)
        if not accept or accept == 'on':
            if not accept:
                messages.error(self.request, _("Please accept the rules"))
                return super(UserCreateView, self).form_invalid(form)
        else:
            messages.error(self.request, _("Wrong input"))
            return super(UserCreateView, self).form_invalid(form)

        form.instance.vazeyat = 1

        if TanzimatPaye.get_settings(ACTIV_MOAREF, False) == '1':
            id_moaref = form.instance.code_moaref_id
            user = User.objects.get(pk=id_moaref)
            max_level = int(TanzimatPaye.get_settings(COUNT_LEVEL_NETWORK, False))
            if user is not None:
                if int(user.sath) + 1 > max_level:
                    messages.error(self.request, _("Level you exceeds max level"))
                    return super(UserCreateView, self).form_invalid(form)
                form.instance.sath = user.sath + 1
                if user.list_parent is not None:
                    jsonDec = json.decoder.JSONDecoder()
                    parents = jsonDec.decode(user.list_parent)
                    parents.insert(0, [user.id])
                    json_parent = json.dumps(parents)
                    new_user = form.save(commit=False)
                    new_user.list_parent = json_parent
                    new_user.save()
                else:
                    parent = []
                    parent.append([user.id])
                    json_parent = json.dumps(parent)
                    new_user = form.save(commit=False)
                    new_user.list_parent = json_parent
                    new_user.save()
            else:
                messages.error(self.request, _("Referral Code is wrong"))
                return super(UserCreateView, self).form_invalid(form)
        else:
            if form.instance.code_moaref is not None:
                id_moaref = form.instance.code_moaref_id
                user = User.objects.get(pk=id_moaref)
                max_level = int(TanzimatPaye.get_settings(COUNT_LEVEL_NETWORK, False))
                if user is not None:
                    if int(user.sath) + 1 > max_level:
                        messages.error(self.request, _("Level you exceeds max level"))
                        return super(UserCreateView, self).form_invalid(form)
                    form.instance.sath = user.sath + 1
                    if user.list_parent is not None:
                        jsonDec = json.decoder.JSONDecoder()
                        parents = jsonDec.decode(user.list_parent)
                        parents.insert(0, [user.id])
                        json_parent = json.dumps(parents)
                        new_user = form.save(commit=False)
                        new_user.list_parent = json_parent
                        new_user.save()
                    else:
                        parent = []
                        parent.append([user.id])
                        json_parent = json.dumps(parent)
                        new_user = form.save(commit=False)
                        new_user.list_parent = json_parent
                        new_user.save()
                else:
                    messages.error(self.request, _("Referral Code is wrong"))
                    return super(UserCreateView, self).form_invalid(form)
            else:
                form.instance.sath = 1
        return super(UserCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return super(UserCreateView, self).form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        referer = self.request.GET.get('referer', None)
        if 'code_moaref' in form.fields and referer:
            form.fields['code_moaref'].widget.attrs['value'] = f"code_{referer}"
        return form

    def get_success_url(self):
        return reverse('login')


def login_user(request):
    if request.user.is_authenticated:
        if request.POST.get('next') is not None:
            return redirect(request.POST.get('next'))
        return redirect('dashboard')
    else:
        a = ReCaptchaField(widget=ReCaptchaV2Checkbox())
        if request.method == "POST":
            if 'g-recaptcha-response' in request.POST:
                try:
                    a.validate(request.POST.get('g-recaptcha-response'))
                except:
                    return render(request, "system/user/login.html",
                                  {'error': _("Invalid Captcha Error"),
                                   "recaptcha": a.widget.render('recaptcha', '')})
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    if request.GET.get('next') is not None:
                        return redirect(request.GET.get('next'))
                    else:
                        return redirect('dashboard')
                else:
                    return render(request, "system/user/login.html",
                                  {'error': _("You are not allowed to access"),
                                   "recaptcha": a.widget.render('recaptcha', '')})
            else:
                return render(request, "system/user/login.html",
                              {'error': _("Username or Password you entered is wrong"),
                               "recaptcha": a.widget.render('recaptcha', '')})
        else:

            return render(request, "system/user/login.html", context={
                "recaptcha": a.widget.render('recaptcha', '')
            })

@login_required
def logout_user(request):
    request.user.last_logout = timezone.now()
    request.user.last_activity = None
    request.user.save()
    logout(request)
    return redirect(reverse('login'))


class RedirectToUserUpdate(LoginRequiredMixin, View):
    def get(self, request):
        return redirect(reverse('UpdateUser', args=[request.user.id]))

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'system/user/Update_User.html'
    form_class = UserUpdateForm

    def form_valid(self, form):
        messages.success(self.request, _("Your changes are committed successfully"))
        return super(UserUpdateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            kwargs['pk'] = request.user.id
        if not request.user.is_superuser and request.user.id != kwargs['pk']:
            messages.error(self.request, _("Your not allowed here"))
            return redirect(reverse('UpdateUser', kwargs={'pk': request.user.id}))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.id != kwargs['pk']:
            messages.error(self.request, _("Your not allowed here"))
            return redirect(reverse('UpdateUser', kwargs={'pk': request.user.id}))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context['form']
        context['form'] = form
        return context

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
            form.fields['mobile'].required = False
            form.fields['email'].required = False
            form.fields['tarikh_tavalod'].required = False
            form.fields['image_cart_melli'].required = False
            form.fields['father_name'].required = False
            form.fields['shomare_hesab'].required = False
            form.fields['shomare_cart'].required = False
            form.fields['shomare_shaba'].required = False
            form.fields['name_saheb_hesab'].required = False
            form.fields['name_bank'].required = False
            form.fields['id_telegram'].required = False
            form.fields['code_posti'].required = False
            form.fields['address'].required = False
        else:
            del form.fields['is_active']
            if self.object.image_cart_melli is not None:
                form.fields['image_cart_melli'].required = False

        return form

class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        try:
            user = get_object_or_404(User, pk=pk)
            if user.tabligh_set.exists():
                messages.error(request, _("This user has Ads"))
                return redirect('ListUser')
            elif User.objects.filter(code_moaref=user).exists():
                messages.error(request, _("This user has referrals"))
                return redirect('ListUser')
            user.delete()
        except ProtectedError:
            messages.error(self.request, _("This is not possible"))
            return redirect('ListUser')
        messages.success(self.request, _("User deleted successfully"))
        return redirect('ListUser')

class UserListView(LoginRequiredMixin, TemplateView):
    template_name = 'system/user/List_User.html'

class UserDatatableView(LoginRequiredMixin, BaseDatatableView):
    model = User
    columns = ['id', 'username', 'first_name', 'last_name', 'code_melli', 'date_joined', 'tarikh_tavalod', 'mobile',
               'gender', 'father_name',
               'is_active', 'online', 'is_superuser']

    def render_column(self, row, column):
        if column == 'tarikh_tavalod':
            return date_jalali(row.tarikh_tavalod, 3)
        if column == 'date_joined':
            return date_jalali(row.date_joined, 3)
        if column == 'online':
            return row.user_status
        if column == 'is_superuser':
            return 1 if row.is_superuser else 0
        return super().render_column(row, column)

    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(username__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search))
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

class ToggleAdminStateView(LoginRequiredMixin, View):
    def get(self, request, id):
        if not request.user.is_superuser:
            messages.error(request, _("You are not allowed to access"))
            return redirect("dashboard")
        if request.user.id != MAIN_ADMIN_ID:
            messages.error(request, _("You are not allowed to access"))
            return redirect("ListUser")
        elif request.user.id == MAIN_ADMIN_ID:
            messages.error(request, _("This is not possible"))
            return redirect("ListUser")
        try:
            user = User.objects.get(id=id)
            user.is_superuser = not user.is_superuser
            user.save()
            if user.is_superuser:
                messages.success(request, _("The user is now an admin"))
            else:
                messages.success(request, "")
            return redirect("ListUser")
        except:
            messages.error(request, _("User does not exists"))
            return redirect("ListUser")
