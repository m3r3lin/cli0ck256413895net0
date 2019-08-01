from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from Ads_Project import settings
from system.functions import upload_avatar_path, upload_cart_melli_path
from django.db.models import Model

VAZEYAT_CHOICES = (
    (1, 'فعال'),
    (0, 'غیرفعال'),
)
VAZEYAT_Tabligh = (
    (0, 'لغو شده'),
    (1, 'فعال'),
    (2, 'در انتظار تایید'),
    (3, 'به اتمام رسیده'),
)
GENDER_CHOICES = (
    (1, 'مرد'),
    (0, 'زن'),
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
    gender = models.IntegerField(null=True, blank=True, choices=GENDER_CHOICES)
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
    code_moaref = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    id_telegram = models.CharField(max_length=30, null=True, blank=True)
    nooe_heshab = models.IntegerField(null=True, blank=True, choices=NOOE_CHOICES)
    vazeyat = models.IntegerField(null=True, blank=True, choices=VAZEYAT_CHOICES)
    image_cart_melli = models.ImageField(upload_to=upload_cart_melli_path, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar_path, null=True, blank=True)

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

    def __str__(self):
        return self.onvan


class Click(Model):
    tabligh = models.ForeignKey(Tabligh, on_delete=models.CASCADE)
    montasher_konande = models.ForeignKey(User, on_delete=models.CASCADE)
    tarikh = models.DateTimeField(default=datetime.now)
    ip = models.CharField(max_length=15)


class Payam(Model):
    ferestande = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ferestande_user_id')
    girande = models.ForeignKey(User, on_delete=models.CASCADE, related_name='girande_user_id')
    onvan = models.CharField(max_length=150)
    text = models.TextField()
    tarikh = models.DateTimeField(auto_now_add=True)
    vazeyat = models.IntegerField(choices=VAZEYAT_PAYAM)


ACTIV_MOAREF = 'active_moaref'


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


if not settings.CREATING_SUPER_USER:
    @receiver(pre_save, sender=User)
    def set_new_user_inactive(sender, instance, **kwargs):
        if instance._state.adding is True:
            instance.password = make_password(instance.password)
