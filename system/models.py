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


class User(AbstractUser):
    GENDER_CHOICES = (
        ('مرد', 'مرد'),
        ('زن', 'زن'),
    )
    NOOE_CHOICES = (
        ('تبلیغ گذار', 'تبلیغ گذار'),
        ('منتشر کننده', 'منتشر کننده'),
        ('هر دو', 'هر دو'),
    )
    VAZEYAT_CHOICES = (
        ('فعال', 'فعال'),
        ('غیرفعال', 'غیرفعال'),
        ('در انتظار', 'در انتظار'),
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    code_melli = models.CharField(max_length=10, null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    father_name = models.CharField(max_length=30, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(blank=True)
    shomare_hesab = models.CharField(max_length=30, null=True, blank=True)
    shomare_cart = models.CharField(max_length=30, null=True, blank=True)
    shomare_shaba = models.CharField(max_length=30, null=True, blank=True)
    name_saheb_hesab = models.CharField(max_length=30, null=True, blank=True)
    name_bank = models.CharField(max_length=30, null=True, blank=True)
    code_posti = models.CharField(max_length=10, null=True, blank=True)
    kife_pool = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    kife_daramad = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    code_moaref = models.CharField(max_length=30)
    tarikh_ozviyat = models.DateTimeField(default=datetime.now, blank=True)
    id_telegram = models.CharField(max_length=30)
    nooe_heshab = models.CharField(max_length=20, choices=NOOE_CHOICES)
    vazeyat = models.CharField(max_length=20, choices=VAZEYAT_CHOICES)
    image_cart_melli = models.ImageField(upload_to=upload_cart_melli_path, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar_path, null=True, blank=True)

    def __str__(self):
        return self.username


class Pelan(Model):
    VAZEYAT_CHOICES = (
        ('فعال', 'فعال'),
        ('غیرفعال', 'غیرفعال'),
        ('در انتظار', 'در انتظار'),
    )
    onvan = models.CharField(max_length=30)
    gheymat = models.IntegerField(default=500000, validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    tarikh_ijad = models.DateTimeField(default=datetime.now, blank=True)
    vazeyat = models.CharField(max_length=10, choices=VAZEYAT_CHOICES)

    def __str__(self):
        return self.onvan


class Tabligh(Model):
    VAZEYAT_CHOICES = (
        ('فعال', 'فعال'),
        ('غیرفعال', 'غیرفعال'),
        ('در انتظار', 'در انتظار'),
    )
    onvan = models.CharField(max_length=30)
    code_tabligh_gozaar = models.CharField(max_length=30)
    tarikh_ijad = models.DateTimeField(default=datetime.now, blank=True)
    code_pelan = models.ForeignKey(Pelan, on_delete=models.CASCADE)
    tedad_click = models.IntegerField(default=0)
    tedad_click_shode = models.IntegerField(default=0)
    link = models.CharField(max_length=500)
    vazeyat = models.CharField(max_length=10, choices=VAZEYAT_CHOICES)

    def __str__(self):
        return self.onvan


if not settings.CREATING_SUPER_USER:
    @receiver(pre_save, sender=User)
    def set_new_user_inactive(sender, instance, **kwargs):
        if instance._state.adding is True:
            instance.password = make_password(instance.password)
