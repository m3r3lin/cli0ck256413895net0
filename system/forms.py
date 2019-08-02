import re

from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileInput
from django import forms
from unidecode import unidecode

from system.functions import change_date_to_english
from system.models import User, Pelan, Tabligh, TanzimatPaye, ACTIV_MOAREF
from django.forms.widgets import ClearableFileInput

fullmatch_compiled = re.compile('^code_(\d{1,9})')


class MyClearableFileInput(FileInput):
    initial_text = "تصویر فعلی"
    input_text = 'عوض کردن'
    clear_checkbox_label = 'پاک کردن'


class TanzimatPayeMiddelware(ModelForm):

    def add_field(self, field_name):
        if field_name not in self.Meta.fields:
            self.Meta.fields.append(field_name)

    def remove_field(self, field_name):
        if field_name in self.Meta.fields:
            del self.Meta.fields[field_name]

    def add_field_message(self, field_name):
        if field_name not in self.Meta.error_messages:
            self.Meta.error_messages[field_name] = {}

    def add_field_message_error(self, field_name, key, value):
        self.add_field_message(field_name)
        self.Meta.error_messages[field_name][key] = value

    def add_field_message_error_direct(self, field_name, key, value):
        if field_name in self.fields:
            self.fields[field_name].error_messages[key] = value

    def after_init(self):
        if 'code_moaref' in self.Meta.fields:
            if not hasattr(self, 'clean_code_moaref'):
                setattr(self, 'clean_code_moaref', self.validate_code_moarefi)
            try:
                active_moarefi = int(TanzimatPaye.get_settings(ACTIV_MOAREF, 0))
                if active_moarefi:
                    self.fields['code_moaref'].required = True
                    self.add_field_message_error_direct('code_moaref', 'required', "کد معرف اجباری است!")
                else:
                    self.fields['code_moaref'].required = False
            except:
                pass

    def validate_code_moarefi(self):
        c = self.cleaned_data['code_moaref']
        active_moarefi = int(TanzimatPaye.get_settings(ACTIV_MOAREF, 0))
        if active_moarefi and c:
            fullmatch = fullmatch_compiled.fullmatch(c)
            if fullmatch:
                c = fullmatch.groups()[0]
                if c.isdigit():
                    try:
                        return User.objects.get(pk=int(c))
                    except User.DoesNotExist:
                        pass
            raise forms.ValidationError('کد معرف اشتباه است')
        else:
            return None


class UserCreateForm(TanzimatPayeMiddelware):
    # username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}), error_messages={})
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}))
    mobile = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'موبایل'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}))
    password = forms.CharField(widget=forms.PasswordInput(), error_messages={'required': "پسورد اجباری است!"})
    code_moaref = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'کد معرف'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'mobile', 'email', 'password', 'code_moaref']
        error_messages = {
            'username': {
                'invalid': "فرمت نام کاریری اشتباه است",
                'unique': "این نام کاربری قبلا ثبت شده است!",
                'required': "نام کاربری است!",
            },
            'first_name': {
                'required': "نام است!",
            },
            'last_name': {
                'required': "نام خانوادگی است!",
            },
            'mobile': {
                'required': "موبایل اجباری است!",
            },
            'email': {
                'required': "ایمیل اجباری است!",
            },
            'password': {
                'required': "پسورد اجباری است!",
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "نام کاربری:"
        self.fields['username'].required = True
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'id': 'username', 'placeholder': 'نام کاربری'})

        self.fields['first_name'].label = "نام:"
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'id': 'full_name'})

        self.fields['last_name'].label = "نام خانوادگی:"
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'id': 'full_name'})

        self.fields['mobile'].label = "موبایل:"
        self.fields['mobile'].required = True
        self.fields['mobile'].widget.attrs.update({'class': 'form-control', 'id': 'password'})

        self.fields['email'].label = "ایمیل:"
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'id': 'gmail'})

        self.fields['password'].label = "رمز عبور:"
        self.fields['password'].required = True
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'id': 'password'})

        self.fields['code_moaref'].label = "کد معرف:"
        self.fields['code_moaref'].required = True
        self.fields['code_moaref'].widget.attrs.update({'class': 'form-control', 'id': 'code_moaref'})

        self.after_init()


class UserUpdateForm(TanzimatPayeMiddelware):
    tarikh_tavalod = forms.CharField(required=False)
    avatar = forms.ImageField(required=False, widget=MyClearableFileInput)
    image_cart_melli = forms.ImageField(required=False, widget=MyClearableFileInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'code_melli', 'tarikh_tavalod', 'mobile', 'gender', 'father_name', 'address', 'email', 'shomare_hesab',
                  'shomare_cart', 'shomare_shaba', 'name_saheb_hesab', 'name_bank', 'code_posti', 'kife_pool', 'kife_daramad',
                  'code_moaref', 'sath', 'id_telegram', 'nooe_heshab', 'vazeyat', 'image_cart_melli', 'avatar']
        error_messages = {
            'first_name': {
                'required': "نام اجباری است!",
            },
            'last_name': {
                'required': "نام خانوادگی اجباری است!",
            },
            'code_melli': {
                'unique': "این شماره ملی قبلا ثبت شده است!",
                'required': "کد ملی اجباری است!",
            },
            'tarikh_tavalod': {
                'required': "تاریخ تولد اجباری است!",
            },
            'mobile': {
                'required': "موبایل اجباری است!",
            },
            'gender': {
                'required': "جنسیت اجباری است!",
            },
            'father_name': {
                'required': "نام پدر اجباری است!",
            },
            'address': {
                'required': "آدرس اجباری است!",
            },
            'email': {
                'required': "ایمیل اجباری است!",
            },
            'shomare_hesab': {
                'unique': "این شماره حساب قبلا ثبت شده است!",
                'required': "شماره حساب اجباری است!",
            },
            'shomare_cart': {
                'unique': "این شماره کارت قبلا ثبت شده است!",
                'required': "شماره کارت اجباری است!",
            },
            'shomare_shaba': {
                'unique': "این شماره شبا قبلا ثبت شده است!",
                'required': "شماره شبا اجباری است!",
            },
            'name_saheb_hesab': {
                'required': "نام صاحب حساب اجباری است!",
            },
            'name_bank': {
                'required': "نام بانک اجباری است!",
            },
            'code_posti': {
                'required': "کدپستی اجباری است!",
            },
            'kife_pool': {
                'required': "کیف پول اجباری است!",
            },
            'kife_daramad': {
                'required': "کیف درآمد اجباری است!",
            },
            'code_moaref': {
                'required': ("کد معرف اجباری است!"),
            },
            'sath': {
                'required': ("سطح اجباری است!"),
            },
            'id_telegram': {
                'required': "آی دی تلگرام اجباری است!",
            },
            'nooe_heshab': {
                'required': "نوع حساب اجباری است!",
            },
            'vazeyat': {
                'required': "وضعیت اجباری است!",
            },
            'image_cart_melli': {
                'required': "تصویر کارت ملی اجباری است!",
            },
            'avatar': {
                'required': "آواتار اجباری است!",
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "نام:"
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'id': 'full_name'})

        self.fields['last_name'].label = "نام خانوادگی:"
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'id': 'full_name'})

        self.fields['code_melli'].label = "کد ملی:"
        self.fields['code_melli'].required = True
        self.fields['code_melli'].widget.attrs.update({'class': 'form-control', 'id': 'code_melli'})

        self.fields['tarikh_tavalod'].label = "تاریخ تولد:"
        self.fields['tarikh_tavalod'].required = False
        self.fields['tarikh_tavalod'].widget.attrs.update({'class': 'form-control', 'id': 'tarikh_tavalod'})

        self.fields['mobile'].label = "موبایل:"
        self.fields['mobile'].required = True
        self.fields['mobile'].widget.attrs.update({'class': 'form-control', 'id': 'mobile'})

        self.fields['gender'].label = "جنسیت:"
        self.fields['gender'].required = True
        self.fields['gender'].widget.attrs.update({'class': 'form-control', 'id': 'gender'})

        self.fields['father_name'].label = "نام پدر:"
        self.fields['father_name'].required = True
        self.fields['father_name'].widget.attrs.update({'class': 'form-control', 'id': 'father_name'})

        self.fields['address'].label = "آدرس:"
        self.fields['address'].required = True
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'id': 'address'})

        self.fields['email'].label = "ایمیل:"
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'id': 'email'})

        self.fields['shomare_hesab'].label = "شماره حساب:"
        self.fields['shomare_hesab'].required = True
        self.fields['shomare_hesab'].widget.attrs.update({'class': 'form-control', 'id': 'shomare_hesab'})

        self.fields['shomare_cart'].label = "شماره کارت:"
        self.fields['shomare_cart'].required = True
        self.fields['shomare_cart'].widget.attrs.update({'class': 'form-control', 'id': 'shomare_cart'})

        self.fields['shomare_shaba'].label = "شماره شبا:"
        self.fields['shomare_shaba'].required = True
        self.fields['shomare_shaba'].widget.attrs.update({'class': 'form-control', 'id': 'shomare_shaba'})

        self.fields['name_saheb_hesab'].label = "نام صاحب حساب:"
        self.fields['name_saheb_hesab'].required = True
        self.fields['name_saheb_hesab'].widget.attrs.update({'class': 'form-control', 'id': 'name_saheb_hesab'})

        self.fields['name_bank'].label = "نام بانک:"
        self.fields['name_bank'].required = True
        self.fields['name_bank'].widget.attrs.update({'class': 'form-control', 'id': 'name_bank'})

        self.fields['code_posti'].label = "کدپستی:"
        self.fields['code_posti'].required = True
        self.fields['code_posti'].widget.attrs.update({'class': 'form-control', 'id': 'code_posti'})

        self.fields['kife_pool'].label = "کیف پول:"
        self.fields['kife_pool'].required = False
        self.fields['kife_pool'].widget.attrs.update({'class': 'form-control', 'id': 'kife_pool'})

        self.fields['kife_daramad'].label = "کیف درآمد:"
        self.fields['kife_daramad'].required = False
        self.fields['kife_daramad'].widget.attrs.update({'class': 'form-control', 'id': 'kife_daramad'})

        self.fields['code_moaref'].label = "کد معرف:"
        self.fields['code_moaref'].required = True
        self.fields['code_moaref'].widget.attrs.update({'class': 'form-control', 'id': 'code_moaref'})

        self.fields['sath'].label = "سطح:"
        self.fields['sath'].required = True
        self.fields['sath'].widget.attrs.update({'class': 'form-control', 'id': 'sath'})

        self.fields['id_telegram'].label = "آی دی تلگرام:"
        self.fields['id_telegram'].required = False
        self.fields['id_telegram'].widget.attrs.update({'class': 'form-control', 'id': 'id_telegram'})

        self.fields['nooe_heshab'].label = "نوع حساب:"
        self.fields['nooe_heshab'].required = True
        self.fields['nooe_heshab'].widget.attrs.update({'class': 'form-control', 'id': 'nooe_heshab'})

        self.fields['vazeyat'].label = "وضعیت:"
        self.fields['vazeyat'].required = True
        self.fields['vazeyat'].widget.attrs.update({'class': 'form-control', 'id': 'vazeyat'})

        self.fields['image_cart_melli'].label = "تصویر کارت ملی:"
        self.fields['image_cart_melli'].required = True
        self.fields['image_cart_melli'].widget.attrs.update({'class': 'form-control', 'id': 'image_cart_meli'})

        self.fields['avatar'].label = "آواتار:"
        self.fields['avatar'].required = False
        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'id': 'avatar'})

        self.after_init()

    def clean_tarikh_tavalod(self):
        tarikh_tavalod = self.cleaned_data['tarikh_tavalod']
        if tarikh_tavalod == '':
            raise ValidationError("فیلد تاریخ تولد اجباری است.")
        r = re.compile('\d\d\d\d/\d\d/\d{1,2}')
        if tarikh_tavalod != None and tarikh_tavalod != '':
            if (r.match(unidecode(tarikh_tavalod)) is None):
                raise ValidationError("فرمت تاریخ تولد اشتباه است!")
        tarikh_tavalod = change_date_to_english(tarikh_tavalod, 2)
        return tarikh_tavalod


class PelanCreateForm(ModelForm):
    class Meta:
        model = Pelan
        fields = ['onvan', 'gheymat', 'tedad_click', 'vazeyat']
        error_messages = {
            'onvan': {
                'unique': "این عنوان قبلا ثبت شده است!",
                'required': "عنوان اجباری است!",
            },
            'gheymat': {
                'required': "قیمت اجباری است!",
            },
            'tedad_click': {
                'required': "تعداد کلیک اجباری است!",
            },
            'vazeyat': {
                'required': "وضعیت اجباری است!",
            },
        }

    def __init__(self, *args, **kwargs):
        super(PelanCreateForm, self).__init__(*args, **kwargs)
        self.fields['onvan'].label = "عنوان:"
        self.fields['onvan'].required = True
        self.fields['onvan'].widget.attrs.update({'class': 'form-control', 'id': 'onvan'})

        self.fields['gheymat'].label = "قیمت:"
        self.fields['gheymat'].required = True
        self.fields['gheymat'].widget.attrs.update({'class': 'form-control', 'id': 'gheymat'})

        self.fields['tedad_click'].label = "تعداد کلیک:"
        self.fields['tedad_click'].required = True
        self.fields['tedad_click'].widget.attrs.update({'class': 'form-control', 'id': 'tedad_click'})

        self.fields['vazeyat'].label = "وضعیت:"
        self.fields['vazeyat'].required = True
        self.fields['vazeyat'].widget.attrs.update({'class': 'form-control', 'id': 'vazeyat'})


class TablighCreateForm(ModelForm):
    code_pelan = forms.ModelChoiceField(queryset=Pelan.objects.order_by('-onvan'))

    class Meta:
        model = Tabligh
        fields = ['onvan', 'text', 'code_tabligh_gozaar', 'code_pelan', 'tedad_click', 'tedad_click_shode', 'vazeyat']
        error_messages = {
            'onvan': {
                'unique': "این عنوان قبلا ثبت شده است!",
                'required': "عنوان اجباری است!",
            },
            'text': {
                'required': "متن اجباری است!",
            },
            'code_tabligh_gozaar': {
                'required': "کد تبلیغ گذار اجباری است!",
            },
            'code_pelan': {
                'required': "کد پلن اجباری است!",
            },
            'tedad_click': {
                'required': "تعداد کلیک اجباری است!",
            },
            'tedad_click_shode': {
                'required': "تعداد کلیک شده اجباری است!",
            },
            'vazeyat': {
                'required': "وضعیت اجباری است!",
            },
        }

    def __init__(self, *args, **kwargs):
        super(TablighCreateForm, self).__init__(*args, **kwargs)

        self.fields['onvan'].label = "عنوان:"
        self.fields['onvan'].required = True
        self.fields['onvan'].widget.attrs.update({'class': 'form-control', 'id': 'onvan'})

        self.fields['text'].label = "متن:"
        self.fields['text'].required = True
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'id': 'text'})

        self.fields['code_tabligh_gozaar'].label = "کد تبلیغ گذار:"
        self.fields['code_tabligh_gozaar'].required = True
        self.fields['code_tabligh_gozaar'].widget.attrs.update({'class': 'form-control', 'id': 'code_tabligh_gozaar'})

        self.fields['code_pelan'].label = "عنوان پلن:"
        self.fields['code_pelan'].required = True
        self.fields['code_pelan'].widget.attrs.update({'class': 'form-control', 'id': 'code_pelan'})

        self.fields['tedad_click'].label = "تعداد کلیک:"
        self.fields['tedad_click'].required = True
        self.fields['tedad_click'].widget.attrs.update({'class': 'form-control', 'id': 'tedad_click'})

        self.fields['tedad_click_shode'].label = "تعداد کلیک شده:"
        self.fields['tedad_click_shode'].required = False
        self.fields['tedad_click_shode'].widget.attrs.update({'class': 'form-control', 'id': 'tedad_click_shode'})

        self.fields['vazeyat'].label = "وضعیت:"
        self.fields['vazeyat'].required = False
        self.fields['vazeyat'].widget.attrs.update({'class': 'form-control', 'id': 'vazeyat'})


class ActiveCodeMoarefForm(ModelForm):
    VAZEYAT_CHOICES = (
        ('1', 'فعال'),
        ('0', 'غیرفعال'),
    )
    value = forms.ChoiceField(choices=VAZEYAT_CHOICES)

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(ActiveCodeMoarefForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = "فعال / غیرفعال:"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class SodeModirForm(ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(SodeModirForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = "مقدار:"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class ChangeUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password', ]
        error_messages = {
            'old_password': {
                'password_incorrect': "پسورد شما اشتباه است",
            },
            'new_password1': {
                "password_mismatch": "پسورد های باید یکی باشد"
            },
            'new_password2': {
                "password_mismatch": "پسورد های باید یکی باشد"
            },
        }

    def __init__(self, *args, **kwargs):
        super(ChangeUserPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = 'پسورد'
        self.fields['new_password1'].help_text = ''
