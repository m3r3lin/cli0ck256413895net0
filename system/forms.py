from django.forms import ModelForm
from django import forms
from system.models import User, Pelan
from django.forms.widgets import ClearableFileInput


class MyClearableFileInput(ClearableFileInput):
    initial_text = "تصویر فعلی"
    input_text = 'عوض کردن'
    clear_checkbox_label = 'پاک کردن'


class UserCreateForm(ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}))
    mobile = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'موبایل'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}))
    password = forms.CharField(widget=forms.PasswordInput(), error_messages={'required': "پسورد اجباری است!"})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'mobile', 'email', 'password')
        error_messages = {
            'username': {
                'required': ("نام کاربری است!"),
            },
            'first_name': {
                'required': ("نام است!"),
            },
            'last_name': {
                'required': ("نام خانوادگی است!"),
            },
            'mobile': {
                'required': ("موبایل اجباری است!"),
            },
            'email': {
                'required': ("ایمیل اجباری است!"),
            },
            'password': {
                'required': ("پسورد اجباری است!"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "نام کاربری:"
        self.fields['username'].required = True
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'id': 'username'})

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


class UserUpdateForm(ModelForm):
    # code_melli = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'کد ملی'}))
    # username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}))
    # password = forms.CharField(required=True, widget=forms.PasswordInput())
    # first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام'}))
    # last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'}))
    # mobile = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'موبایل'}))
    # phone = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'تلفن'}))
    # email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}))
    # address = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 4}))
    avatar = forms.ImageField(required=False, widget=MyClearableFileInput)
    image_cart_melli = forms.ImageField(required=False, widget=MyClearableFileInput)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'code_melli', 'mobile', 'gender', 'father_name', 'address', 'email', 'shomare_hesab',
            'shomare_cart', 'shomare_shaba', 'name_saheb_hesab', 'name_bank', 'code_posti', 'kife_pool', 'kife_daramad',
            'code_moaref', 'tarikh_ozviyat', 'id_telegram', 'nooe_heshab', 'vazeyat', 'image_cart_melli', 'avatar')
        error_messages = {
            'first_name': {
                'required': ("نام اجباری است!"),
            },
            'last_name': {
                'required': ("نام خانوادگی اجباری است!"),
            },
            'code_melli': {
                'required': ("کد ملی اجباری است!"),
            },
            'mobile': {
                'required': ("موبایل اجباری است!"),
            },
            'gender': {
                'required': ("جنسیت اجباری است!"),
            },
            'father_name': {
                'required': ("نام پدر اجباری است!"),
            },
            'address': {
                'required': ("آدرس اجباری است!"),
            },
            'email': {
                'required': ("ایمیل اجباری است!"),
            },
            'shomare_hesab': {
                'required': ("شماره حساب اجباری است!"),
            },
            'shomare_cart': {
                'required': ("شماره کارت اجباری است!"),
            },
            'shomare_shaba': {
                'required': ("شماره شبا اجباری است!"),
            },
            'name_saheb_hesab': {
                'required': ("نام صاحب حساب اجباری است!"),
            },
            'name_bank': {
                'required': ("نام بانک اجباری است!"),
            },
            'code_posti': {
                'required': ("کدپستی اجباری است!"),
            },
            'kife_pool': {
                'required': ("کیف پول اجباری است!"),
            },
            'kife_daramad': {
                'required': ("کیف درآمد اجباری است!"),
            },
            'code_moaref': {
                'required': ("کد معرف اجباری است!"),
            },
            'tarikh_ozviyat': {
                'required': ("تاریخ عضویت اجباری است!"),
            },
            'id_telegram': {
                'required': ("آی دی تلگرام اجباری است!"),
            },
            'nooe_heshab': {
                'required': ("نوع حساب اجباری است!"),
            },
            'vazeyat': {
                'required': ("وضعیت اجباری است!"),
            },
            'image_cart_melli': {
                'required': ("تصویر کارت ملی اجباری است!"),
            },
            'avatar': {
                'required': ("آواتار اجباری است!"),
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
        self.fields['kife_pool'].required = True
        self.fields['kife_pool'].widget.attrs.update({'class': 'form-control', 'id': 'kife_pool'})

        self.fields['kife_daramad'].label = "کیف درآمد:"
        self.fields['kife_daramad'].required = True
        self.fields['kife_daramad'].widget.attrs.update({'class': 'form-control', 'id': 'kife_daramad'})

        self.fields['code_moaref'].label = "کد معرف:"
        self.fields['code_moaref'].required = True
        self.fields['code_moaref'].widget.attrs.update({'class': 'form-control', 'id': 'code_moaref'})

        self.fields['tarikh_ozviyat'].label = "تاریخ عضویت:"
        self.fields['tarikh_ozviyat'].required = True
        self.fields['tarikh_ozviyat'].widget.attrs.update({'class': 'form-control', 'id': 'tarikh_ozviyat'})

        self.fields['id_telegram'].label = "آی دی تلگرام:"
        self.fields['id_telegram'].required = True
        self.fields['id_telegram'].widget.attrs.update({'class': 'form-control', 'id': 'id_telegram'})

        self.fields['nooe_heshab'].label = "نوع حساب:"
        self.fields['nooe_heshab'].required = True
        self.fields['nooe_heshab'].widget.attrs.update({'class': 'form-control', 'id': 'nooe_heshab'})

        self.fields['vazeyat'].label = "وضعیت:"
        self.fields['vazeyat'].required = True
        self.fields['vazeyat'].widget.attrs.update({'class': 'form-control', 'id': 'vazeyat'})

        self.fields['image_cart_melli'].label = "تصویر کارت ملی:"
        self.fields['image_cart_melli'].required = False
        self.fields['image_cart_melli'].widget.attrs.update({'class': 'form-control', 'id': 'image_cart_meli'})

        self.fields['avatar'].label = "آواتار:"
        self.fields['avatar'].required = False
        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'id': 'avatar'})


class PelanCreateForm(ModelForm):
    class Meta:
        model = Pelan
        fields = ('onvan', 'gheymat', 'tarikh_ijad', 'vazeyat')
        error_messages = {
            'onvan': {
                'required': ("عنوان اجباری است!"),
            },
            'gheymat': {
                'required': ("قیمت اجباری است!"),
            },
            'tarikh_ijad': {
                'required': ("تاریخ ایجاد اجباری است!"),
            },
            'vazeyat': {
                'required': ("وضعیت اجباری است!"),
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

        self.fields['tarikh_ijad'].label = "تاریخ ایجاد:"
        self.fields['tarikh_ijad'].required = True
        self.fields['tarikh_ijad'].widget.attrs.update({'class': 'form-control', 'id': 'tarikh_ijad'})

        self.fields['vazeyat'].label = "وضعیت:"
        self.fields['vazeyat'].required = True
        self.fields['vazeyat'].widget.attrs.update({'class': 'form-control', 'id': 'vazeyat'})
