import re

from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, FileInput, Form
from django import forms
from django.utils.translation import ugettext_lazy as _
from unidecode import unidecode

from system.functions import change_date_to_english
from system.models import Payam, Infopm
from system.models import User, Pelan, Tabligh, TanzimatPaye, ACTIV_MOAREF

fullmatch_compiled = re.compile('^code_(\d{1,9})')


class MyClearableFileInput(FileInput):
    initial_text = _("Get Current File")
    input_text = _("Change File")
    clear_checkbox_label = _("Delete File")


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
                    self.add_field_message_error_direct('code_moaref', 'required', _("Referral Code is Required"))
                else:
                    self.fields['code_moaref'].required = False
            except:
                pass
        pass

    def validate_code_moarefi(self):
        c = self.cleaned_data['code_moaref']
        # active_moarefi = int(TanzimatPaye.get_settings(ACTIV_MOAREF, 0))
        if c:
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
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _("First Name")}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _("Last Name")}))
    mobile = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _("Mobile")}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': _("Email")}))
    password = forms.CharField(widget=forms.PasswordInput(), error_messages={'required': _("Password is Required")})
    code_moaref = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Referral")}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'mobile', 'email', 'password', 'code_moaref']
        error_messages = {
            'username': {
                'invalid': _("User name format is invalid"),
                'unique': _("This username is not available"),
                'required': _("Username is required")
                ,
            },
            'first_name': {
                'required': _("First Name is Required")
                ,
            },
            'last_name': {
                'required': _("Last Name is Required")
                ,
            },
            'mobile': {
                'required': _("Mobile is Required")
                ,
            },
            'email': {
                'required': _("Email is Required"),
            },
            'password': {
                'required': _("Password is Required"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _("Username") + ":"
        self.fields['username'].required = True
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'id': 'username'})

        self.fields['first_name'].label = _("First Name") + ":"
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'id': 'full_name'})

        self.fields['last_name'].label = _("Last Name") + ":"
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'id': 'full_name'})

        self.fields['mobile'].label = _("Mobile") + ":"
        self.fields['mobile'].required = True
        self.fields['mobile'].widget.attrs.update({'class': 'form-control', 'id': 'password'})

        self.fields['email'].label = _("Email") + ":"
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'id': 'email'})

        self.fields['password'].label = _("Password") + ":"
        self.fields['password'].required = True
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'id': 'password'})

        self.fields['code_moaref'].label = _("Referral") + ":"
        self.fields['code_moaref'].required = True
        self.fields['code_moaref'].widget.attrs.update({'class': 'form-control', 'id': 'code_moaref'})

        self.after_init()


class UserUpdateForm(ModelForm):
    is_active = forms.BooleanField(required=False)
    tarikh_tavalod = forms.CharField(required=False)
    avatar = forms.ImageField(required=False, widget=MyClearableFileInput)
    image_cart_melli = forms.ImageField(required=False, widget=MyClearableFileInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'code_melli', 'tarikh_tavalod', 'mobile', 'gender', 'father_name',
                  'address', 'code_posti', 'shomare_hesab',
                  'shomare_cart', 'shomare_shaba', 'name_saheb_hesab', 'name_bank', 'email', 'id_telegram', 'country',
                  'image_cart_melli', 'avatar', 'is_active']
        error_messages = {
            'first_name': {
                'required': _("First Name is Required"),
            },
            'last_name': {
                'required': _("Last Name is Required"),
            },
            'code_melli': {
                'unique': _("This id number is already used"),
                'required': _("Id number is required"),
            },
            'tarikh_tavalod': {
                'required': _("BirthDate is Required"),
            },
            'mobile': {
                'required': _("Mobile is Required"),
            },
            'gender': {
                'required': _("Gender is Required"),
            },
            'father_name': {
                'required': _("Father Name is Required"),
            },
            'address': {
                'required': _("Address is Required"),
            },
            'code_posti': {
                'required': _("Postal Code is required"),
            },
            'shomare_hesab': {
                'unique': _("Bank Account Number is already used"),
                'required': _("Bank Account Number is Required"),
            },
            'shomare_cart': {
                'unique': _("This Credit Card Number is already used"),
                'required': _("Credit Card Number is required"),
            },
            'shomare_shaba': {
                'unique': _("This IBAN is already in use"),
                'required': _("IBAN is Required"),
            },
            'name_saheb_hesab': {
                'required': _("Bank Account Owner name is Required"),
            },
            'name_bank': {
                'required': _("Bank Name is Required"),
            },
            'email': {
                'required': _("Email is Required"),
            },
            'id_telegram': {
                'required': _("Telegram ID is Required"),
            },
            'image_cart_melli': {
                'required': _("Id Number image is Required"),
            },
            'avatar': {
                'required': _("Avatar is Required"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = _("First Name") + ":"
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'id': 'full_name'})

        self.fields['last_name'].label = _("Last Name") + ":"
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'id': 'full_name'})

        self.fields['code_melli'].label = _("Id number") + ":"
        self.fields['code_melli'].required = True
        self.fields['code_melli'].widget.attrs.update({'class': 'form-control', 'id': 'code_melli'})

        self.fields['tarikh_tavalod'].label = _("BirthDate") + ":"
        self.fields['tarikh_tavalod'].required = True
        self.fields['tarikh_tavalod'].widget.attrs.update({'class': 'form-control', 'id': 'tarikh_tavalod'})

        self.fields['mobile'].label = _("Mobile") + ":"
        self.fields['mobile'].required = True
        self.fields['mobile'].widget.attrs.update({'class': 'form-control', 'id': 'mobile'})

        self.fields['gender'].label = _("Gender") + ":"
        self.fields['gender'].required = True
        self.fields['gender'].widget.attrs.update({'class': 'form-control', 'id': 'gender'})

        self.fields['father_name'].label = _("Father Name") + ":"
        self.fields['father_name'].required = True
        self.fields['father_name'].widget.attrs.update({'class': 'form-control', 'id': 'father_name'})

        self.fields['address'].label = _("Address") + ":"
        self.fields['address'].required = True
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'id': 'address'})

        self.fields['code_posti'].label = _("Postal Code") + ":"
        self.fields['code_posti'].required = True
        self.fields['code_posti'].widget.attrs.update({'class': 'form-control', 'id': 'code_posti'})

        self.fields['shomare_hesab'].label = _("Bank Account Number") + ":"
        self.fields['shomare_hesab'].required = True
        self.fields['shomare_hesab'].widget.attrs.update({'class': 'form-control', 'id': 'shomare_hesab'})

        self.fields['shomare_cart'].label = _("Credit Card Number") + ":"
        self.fields['shomare_cart'].required = True
        self.fields['shomare_cart'].widget.attrs.update({'class': 'form-control', 'id': 'shomare_cart'})

        self.fields['shomare_shaba'].label = _("IBAN") + ":"
        self.fields['shomare_shaba'].required = True
        self.fields['shomare_shaba'].widget.attrs.update({'class': 'form-control', 'id': 'shomare_shaba'})

        self.fields['name_saheb_hesab'].label = _("Bank Account Owner") + ":"
        self.fields['name_saheb_hesab'].required = True
        self.fields['name_saheb_hesab'].widget.attrs.update({'class': 'form-control', 'id': 'name_saheb_hesab'})

        self.fields['name_bank'].label = _("Bank Name") + ":"
        self.fields['name_bank'].required = True
        self.fields['name_bank'].widget.attrs.update({'class': 'form-control', 'id': 'name_bank'})

        self.fields['email'].label = _("Email") + ":"
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'id': 'email'})

        self.fields['id_telegram'].label = _("Telegram ID") + ":"
        self.fields['id_telegram'].required = False
        self.fields['id_telegram'].widget.attrs.update({'class': 'form-control', 'id': 'id_telegram'})

        self.fields['image_cart_melli'].label = _("Id Card image") + ":"
        self.fields['image_cart_melli'].required = True
        self.fields['image_cart_melli'].widget.attrs.update({'class': 'form-control', 'id': 'image_cart_meli'})

        self.fields['avatar'].label = _("Avatar") + ":"
        self.fields['avatar'].required = False
        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'id': 'avatar'})

        self.fields['country'].label = _("Country") + ":"
        self.fields['country'].required = False
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'id': 'avatar'})

        self.fields['is_active'].label = _("User State (Activate/Deactivate)") + ":"
        self.fields['is_active'].required = False

    def clean_tarikh_tavalod(self):
        tarikh_tavalod = self.cleaned_data['tarikh_tavalod']
        if tarikh_tavalod == '':
            raise ValidationError(_("BirthDate is Required"))
        r = re.compile('\d\d\d\d/\d\d/\d{1,2}')
        if tarikh_tavalod != None and tarikh_tavalod != '':
            if (r.match(unidecode(tarikh_tavalod)) is None):
                raise ValidationError(_("BirthDate format is wrong"))
        tarikh_tavalod = change_date_to_english(tarikh_tavalod, 2)
        return tarikh_tavalod


class PelanCreateForm(ModelForm):
    class Meta:
        model = Pelan
        fields = ['onvan', 'gheymat', 'tedad_click', 'vazeyat']
        error_messages = {
            'onvan': {
                'unique': _("Title already exists"),
                'required': _("Title is required"),
            },
            'gheymat': {
                'required': _("Price is required"),
            },
            'tedad_click': {
                'required': _("Click Mount is required"),
            },
            'vazeyat': {
                'required': _("Status is required"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(PelanCreateForm, self).__init__(*args, **kwargs)
        self.fields['onvan'].label = _("Title") + ":"
        self.fields['onvan'].required = True
        self.fields['onvan'].widget.attrs.update({'class': 'form-control', 'id': 'onvan'})

        self.fields['gheymat'].label = _("Price") + ":"
        self.fields['gheymat'].required = True
        self.fields['gheymat'].widget.attrs.update({'class': 'form-control', 'id': 'gheymat', 'min': 0})

        self.fields['tedad_click'].label = _("Click Mount") + ":"
        self.fields['tedad_click'].required = True
        self.fields['tedad_click'].widget.attrs.update({'class': 'form-control', 'id': 'tedad_click', 'min': 0})

        self.fields['vazeyat'].label = _("Status") + ":"
        self.fields['vazeyat'].required = True
        self.fields['vazeyat'].widget.attrs.update({'class': 'form-control', 'id': 'vazeyat'})


class TablighCreateForm(ModelForm):
    code_pelan = forms.ModelChoiceField(queryset=Pelan.objects.order_by('-onvan'))

    class Meta:
        model = Tabligh
        fields = ['onvan', 'text', 'code_tabligh_gozaar', 'code_pelan', 'tedad_click', 'tedad_click_shode', 'vazeyat']
        error_messages = {
            'onvan': {
                'unique': _("Title already exists"),
                'required': _("Title is required"),
            },
            'text': {
                'required': _("Text is required"),
            },
            'code_tabligh_gozaar': {
                'required': _("Ad Creator is required"),
            },
            'code_pelan': {
                'required': _("Ad Plan is required"),
            },
            'tedad_click': {
                'required': _("Click Mount is required"),
            },
            'tedad_click_shode': {
                'required': _("Clicked Mount is required"),
            },
            'vazeyat': {
                'required': _("Status is required"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(TablighCreateForm, self).__init__(*args, **kwargs)

        self.fields['onvan'].label = _("Title") + ":"
        self.fields['onvan'].required = True
        self.fields['onvan'].widget.attrs.update({'class': 'form-control', 'id': 'onvan'})

        self.fields['text'].label = _("Text") + ":"
        self.fields['text'].required = True
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'id': 'text'})

        self.fields['code_tabligh_gozaar'].label = _("Ad Creator") + ":"
        self.fields['code_tabligh_gozaar'].required = True
        self.fields['code_tabligh_gozaar'].widget.attrs.update({'class': 'form-control', 'id': 'code_tabligh_gozaar'})

        self.fields['code_pelan'].label = _("Ad Plan Title") + ":"
        self.fields['code_pelan'].required = True
        self.fields['code_pelan'].widget.attrs.update({'class': 'form-control', 'id': 'code_pelan'})

        self.fields['tedad_click'].label = _("Click Mount") + ":"
        self.fields['tedad_click'].required = True
        self.fields['tedad_click'].widget.attrs.update({'class': 'form-control', 'id': 'tedad_click', 'min': 0})

        self.fields['tedad_click_shode'].label = _("Clicked Mount") + ":"
        self.fields['tedad_click_shode'].required = False
        self.fields['tedad_click_shode'].widget.attrs.update(
            {'class': 'form-control', 'id': 'tedad_click_shode', 'min': 0})

        self.fields['vazeyat'].label = _("Status") + ":"
        self.fields['vazeyat'].required = False
        self.fields['vazeyat'].widget.attrs.update({'class': 'form-control', 'id': 'vazeyat'})


class ActiveCodeMoarefForm(ModelForm):
    VAZEYAT_CHOICES = (
        ('1', _("activate")),
        ('0', _("deactivate")),
    )
    value = forms.ChoiceField(choices=VAZEYAT_CHOICES)

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(ActiveCodeMoarefForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Activate / Deactivate") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class ClickIsChangeAbleForm(ModelForm):
    VAZEYAT_CHOICES = (
        ('1', _("activate")),
        ('0', _("deactivate")),
    )
    value = forms.ChoiceField(choices=VAZEYAT_CHOICES)

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(ClickIsChangeAbleForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Activate / Deactivate")
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class LeastBalanceRequiredForm(ModelForm):
    value = forms.IntegerField(error_messages={
        'required': _("Least mount of money is required"),
    })

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(LeastBalanceRequiredForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Least mount of money") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Languge_siteForm(ModelForm):
    VAZEYAT_CHOICES = (
        ('1', _("Persian")),
        ('0', _("English")),
    )
    value = forms.ChoiceField(choices=VAZEYAT_CHOICES)

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Languge_siteForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Persian / English") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class SodeModirForm(ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(SodeModirForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Value") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Count_level_networkForm(ModelForm):
    value = forms.IntegerField(required=True, error_messages={
        'required': _("Percentage is required"),
    })
    onvan = forms.IntegerField(required=True, error_messages={
        'required': _("Title is required"),
    })

    class Meta:
        model = TanzimatPaye
        fields = ['onvan', 'value']

    def __init__(self, *args, **kwargs):
        super(Count_level_networkForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Value") + "مقدار:"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})

        self.fields['onvan'].label = _("Level") + ":"
        self.fields['onvan'].required = True
        self.fields['onvan'].widget.attrs.update({'class': 'form-control', 'id': 'onvan'})


class Count_kharid_hadaghalForm(ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Count_kharid_hadaghalForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Value") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Count_visit_tabligh_Form(ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Count_visit_tabligh_Form, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Value") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Time_kharid_termForm(ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Time_kharid_termForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Value") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Taien_meghdar_matlabForm(ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Taien_meghdar_matlabForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Value") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Show_amarforuserForm(ModelForm):
    VAZEYAT_CHOICES = (
        ('1', _("activate")),
        ('0', _("deactivate")),
    )
    value = forms.ChoiceField(choices=VAZEYAT_CHOICES)

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Show_amarforuserForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Activate / Deactivate") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Taied_khodkar_tablighForm(ModelForm):
    VAZEYAT_CHOICES = (
        ('1', _("activate")),
        ('0', _("deactivate")),
    )
    value = forms.ChoiceField(choices=VAZEYAT_CHOICES)

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Taied_khodkar_tablighForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Activate / Deactivate") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class ChangeUserPasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['password', ]
        error_messages = {
            'old_password': {
                'password_incorrect': _("Incorrect Password"),
            },
            'new_password1': {
                "password_mismatch": _("Password Mismatch"),
            },
            'new_password2': {
                "password_mismatch": _("Password Mismatch"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(ChangeUserPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].label = _("Password") + ':'
        self.fields['new_password1'].help_text = ''


class NewMessageCreateForm(ModelForm):
    class Meta:
        model = Payam
        fields = ['text']
        exclude = ['girande']

    def __init__(self, *args, **kwargs):
        super(NewMessageCreateForm, self).__init__(*args, **kwargs)

        field_name = 'text'
        self.fields[field_name].label = _("Message Text") + ":"
        self.fields[field_name].required = True
        self.fields[field_name].help_text = _("Please Enter Message Text")
        self.fields[field_name].widget.attrs.update({'class': 'form-control', 'id': field_name})


class Vahed_poll_siteForm(ModelForm):
    VAZEYAT_CHOICES = (
        ('1', _("Toman")),
        ('0', _("USD")),
    )
    value = forms.ChoiceField(choices=VAZEYAT_CHOICES)

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Vahed_poll_siteForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("IRT / USD") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Taien_hadaghal_etbarForm(ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(Taien_hadaghal_etbarForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Value") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class MaxNetworkCountForm(ModelForm):
    value = forms.IntegerField()

    class Meta:
        model = TanzimatPaye
        fields = ['value']

    def __init__(self, *args, **kwargs):
        super(MaxNetworkCountForm, self).__init__(*args, **kwargs)

        self.fields['value'].label = _("Value") + ":"
        self.fields['value'].required = True
        self.fields['value'].widget.attrs.update({'class': 'form-control', 'id': 'value'})


class Amar_jaali_Form(Form):
    count_user_online = forms.IntegerField()
    count_all_user = forms.IntegerField()
    count_user_new_today = forms.IntegerField()
    meghdar_daramad_pardahkti = forms.IntegerField()
    count_tabligh_thabti = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(Amar_jaali_Form, self).__init__(*args, **kwargs)

        self.fields['count_user_online'].label = _("Number of online users") + ":"
        self.fields['count_user_online'].required = True
        self.fields['count_user_online'].widget.attrs.update({'class': 'form-control', 'id': 'count_user_online'})

        self.fields['count_all_user'].label = _("Number of users") + ":"
        self.fields['count_all_user'].required = True
        self.fields['count_all_user'].widget.attrs.update({'class': 'form-control', 'id': 'count_all_user'})

        self.fields['count_user_new_today'].label = _("Today's new users count") + ":"
        self.fields['count_user_new_today'].required = True
        self.fields['count_user_new_today'].widget.attrs.update(
            {'class': 'form-control', 'id': 'count_user_new_today'})

        self.fields['meghdar_daramad_pardahkti'].label = _("Paid Income") + ":"
        self.fields['meghdar_daramad_pardahkti'].required = True
        self.fields['meghdar_daramad_pardahkti'].widget.attrs.update(
            {'class': 'form-control', 'id': 'meghdar_daramad_pardahkti'})

        self.fields['count_tabligh_thabti'].label = _("All Created Ads") + ":"
        self.fields['count_tabligh_thabti'].required = True
        self.fields['count_tabligh_thabti'].widget.attrs.update(
            {'class': 'form-control', 'id': 'count_tabligh_thabti'})


class IncreaseBalanceFrom(forms.Form):
    how_much = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_name = 'how_much'
        self.fields[field_name].label = _("Enter In Toman") + ":"
        self.fields[field_name].required = True
        self.fields[field_name].widget.attrs.update({'class': 'form-control', 'id': field_name})

    def clean_how_much(self):
        how_much = self.cleaned_data['how_much']
        if how_much > 0:
            return how_much
        else:
            raise forms.ValidationError(_("Entered Value is Invalid"))


class Create_Infopm(ModelForm):
    class Meta:
        model = Infopm
        fields = ['is_active', 'body']

    def __init__(self, *args, **kwargs):
        super(Create_Infopm, self).__init__(*args, **kwargs)

        self.fields['body'].label = _("Message Text") + ":"
        self.fields['body'].required = True
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'id': 'body', 'rows': 6})

        self.fields['is_active'].label = _("Activate / Deactivate") + ":"
        self.fields['is_active'].required = False
