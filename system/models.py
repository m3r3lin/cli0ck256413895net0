from datetime import datetime

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from Ads_Project import settings
from system.functions import upload_avatar_path, upload_cart_melli_path
from django.db.models import Model, Q
from django.utils import timezone
from allauth.account import signals

VAZEYAT_CHOICES = (
    (0, 'غیرفعال'),
    (1, 'فعال'),
)
VAZEYAT_Tabligh = (
    (0, 'غیرفعال'),
    (1, 'فعال'),
    (2, 'لغو شده'),
    (3, 'در انتظار تایید'),
    (4, 'به اتمام رسیده'),
)
GENDER_CHOICES = (
    (0, 'زن'),
    (1, 'مرد'),
    (2, 'نا مشخص'),
)
NOOE_CHOICES = (
    (0, 'تبلیغ گذار'),
    (1, 'منتشر کننده'),
    (2, 'هر دو'),
)
VAZEYAT_PAYAM = (
    (0, 'خوانده شده'),
    (1, 'خوانده نشده'),
    (2, 'ارسال شده'),
)


class User(AbstractUser):
    code_melli = models.CharField(max_length=10, unique=True, null=True, blank=True)
    tarikh_tavalod = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    gender = models.IntegerField(default=3, null=True, blank=True, choices=GENDER_CHOICES)
    father_name = models.CharField(max_length=35, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    shomare_hesab = models.CharField(max_length=20, unique=True, null=True, blank=True)
    shomare_cart = models.CharField(max_length=20, unique=True, null=True, blank=True)
    shomare_shaba = models.CharField(max_length=24, unique=True, null=True, blank=True)
    name_saheb_hesab = models.CharField(max_length=80, null=True, blank=True)
    name_bank = models.CharField(max_length=80, null=True, blank=True)
    code_posti = models.CharField(max_length=10, null=True, blank=True)
    kife_pool = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999, message='کیف پول نمیتواند بیشتر از 9999999999 باشد. ')])
    kife_daramad = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999, message='کیف درآمد نمیتواند بیشتر از 9999999999 باشد. ')])
    code_moaref = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)
    sath = models.IntegerField(default=1, null=True, blank=True)
    id_telegram = models.CharField(max_length=30, null=True, blank=True)
    nooe_heshab = models.IntegerField(null=True, blank=True, choices=NOOE_CHOICES)
    vazeyat = models.IntegerField(null=True, blank=True, choices=VAZEYAT_CHOICES)
    image_cart_melli = models.ImageField(upload_to=upload_cart_melli_path, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar_path, null=True, blank=True)

    def is_complete(self):
        if self.first_name is not None or\
                self.last_name is not None or\
                self.code_melli is not None or\
                self.tarikh_tavalod is not None or\
                self.mobile is not None or\
                self.gender is not None or \
                self.father_name is not None or \
                self.address is not None or \
                self.code_posti is not None or \
                self.shomare_hesab is not None or \
                self.shomare_cart is not None or \
                self.shomare_shaba is not None or \
                self.name_saheb_hesab is not None or \
                self.name_bank is not None or \
                self.email is not None or \
                self.image_cart_melli is not None:
            return False
        return True

    @staticmethod
    def get_all_not_complete():
        return User.objects.filter(Q(code_melli__isnull=True) |
                                   Q(tarikh_tavalod__isnull=True) |
                                   Q(gender__isnull=True) |
                                   Q(father_name__isnull=True) |
                                   Q(address__isnull=True) |
                                   Q(shomare_hesab__isnull=True) |
                                   Q(shomare_cart__isnull=True) |
                                   Q(shomare_shaba__isnull=True) |
                                   Q(name_saheb_hesab__isnull=True) |
                                   Q(name_bank__isnull=True) |
                                   Q(code_posti__isnull=True) |
                                   Q(image_cart_melli__isnull=True)
                                   )

    def __str__(self):
        return self.username


class Pelan(Model):
    onvan = models.CharField(max_length=80, unique=True)
    gheymat = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    tarikh_ijad = models.DateTimeField(auto_now_add=True)
    tedad_click = models.IntegerField()
    vazeyat = models.IntegerField(choices=VAZEYAT_CHOICES)

    def __str__(self):
        return self.onvan


class Tabligh(Model):
    onvan = models.CharField(max_length=80)
    text = models.TextField()
    code_tabligh_gozaar = models.ForeignKey(User, on_delete=models.CASCADE)
    tarikh_ijad = models.DateTimeField(auto_now_add=True)
    code_pelan = models.ForeignKey(Pelan, on_delete=models.CASCADE)
    tedad_click = models.IntegerField()
    tedad_click_shode = models.IntegerField(default=0)
    vazeyat = models.IntegerField(choices=VAZEYAT_Tabligh)
    mablagh_har_click = models.PositiveIntegerField()

    def __str__(self):
        return self.onvan


class Click(Model):
    tabligh = models.ForeignKey(Tabligh, on_delete=models.CASCADE)
    montasher_konande = models.ForeignKey(User, on_delete=models.CASCADE)
    tarikh = models.DateTimeField(default=datetime.now)
    mablagh_har_click = models.PositiveIntegerField()
    ip = models.CharField(max_length=15)


class Payam(Model):
    ferestande = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ferestande_user_id')
    girande = models.ForeignKey(User, on_delete=models.CASCADE, related_name='girande_user_id')
    onvan = models.CharField(max_length=150)
    text = models.TextField()
    tarikh = models.DateTimeField(auto_now_add=True)
    vazeyat = models.IntegerField(choices=VAZEYAT_PAYAM)
    save_date = models.DateTimeField(default=timezone.now, blank=True, null=True)


ACTIV_MOAREF = 'active_moaref'
LANGUGE_SITE = 'languge_site'
COUNT_LEVEL_NETWORK = 'count_level_network'
COUNT_KHARI_HADAGHAL = 'count_kharid_hadaghl'
TIME_KHARID_TERM = 'time_kharid_term'
TAIEN_MEGHDAR_MATLAB = 'taien_meghdar_matlab'
SHOW_AMAR_FOR_USER = 'show_amar_for_user'
TAIED_KHODKAR_TABLIGH = 'taied_khodkar_tabligh'
TEDAD_SATH_SHABAKE = 'tedad_sath_shabake'


class TanzimatPaye(Model):
    onvan = models.CharField(max_length=250, unique=True)
    value = models.CharField(max_length=250)

    @staticmethod
    def get_settings(key, default=None):
        try:
            return TanzimatPaye.objects.get(onvan=key).value
        except:
            return default


class Parent(Model):
    node = models.ForeignKey(User, on_delete=models.CASCADE, related_name='node_user_id')
    parent = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='parent_user_id')


class TablighatMontasherKonande(Model):
    tabligh = models.ForeignKey(Tabligh, on_delete=models.CASCADE)
    montasher_konande = models.ForeignKey(User, models.CASCADE)
    tarikh = models.DateTimeField(auto_now_add=True)


if not settings.CREATING_SUPER_USER:
    @receiver(pre_save, sender=User)
    def set_new_user_inactive(sender, instance, **kwargs):
        if instance._state.adding is True:
            instance.password = make_password(instance.password)


@receiver(signals.user_logged_in)
def password_change_callback(sender, request, user, **kwargs):
    pass


@receiver(signals.user_logged_out)
def password_change_callback(sender, request, user, **kwargs):
    pass
