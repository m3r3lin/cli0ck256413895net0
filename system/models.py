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
    ('فعال', 'فعال'),
    ('غیرفعال', 'غیرفعال'),
)


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
    code_melli = models.CharField(max_length=10, unique=True, null=True, blank=True)
    tarikh_tavalod = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER_CHOICES)
    father_name = models.CharField(max_length=30, null=True, blank=True)
    address = models.TextField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    shomare_hesab = models.CharField(max_length=30, null=True, blank=True)
    shomare_cart = models.CharField(max_length=30, null=True, blank=True)
    shomare_shaba = models.CharField(max_length=30, null=True, blank=True)
    name_saheb_hesab = models.CharField(max_length=30, null=True, blank=True)
    name_bank = models.CharField(max_length=30, null=True, blank=True)
    code_posti = models.CharField(max_length=10, null=True, blank=True)
    kife_pool = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999, message='کیف پول نمیتواند بیشتر از 9999999999 باشد. ')])
    kife_daramad = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(9999999999, message='کیف درآمد نمیتواند بیشتر از 9999999999 باشد. ')])
    code_moaref = models.CharField(max_length=30, null=True, blank=True)
    tarikh_ozviyat = models.DateTimeField(default=datetime.now, null=True, blank=True)
    id_telegram = models.CharField(max_length=30, null=True, blank=True)
    nooe_heshab = models.CharField(max_length=20, null=True, blank=True, choices=NOOE_CHOICES)
    vazeyat = models.CharField(max_length=20, null=True, blank=True, choices=VAZEYAT_CHOICES)
    image_cart_melli = models.ImageField(upload_to=upload_cart_melli_path, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar_path, null=True, blank=True)

    def __str__(self):
        return self.username


class Pelan(Model):
    onvan = models.CharField(max_length=30, unique=True)
    gheymat = models.IntegerField(default=500000, validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    tarikh_ijad = models.DateTimeField(default=datetime.now, null=True, blank=True)
    tedad_click = models.IntegerField(default=0)
    vazeyat = models.CharField(max_length=10, choices=VAZEYAT_CHOICES)

    def __str__(self):
        return self.onvan


class Tabligh(Model):
    onvan = models.CharField(max_length=30, unique=True)
    text = models.TextField(null=True, blank=True)
    code_tabligh_gozaar = models.ForeignKey(User, on_delete=models.CASCADE)
    tarikh_ijad = models.DateTimeField(default=datetime.now, null=True, blank=True)
    code_pelan = models.ForeignKey(Pelan, on_delete=models.CASCADE)
    tedad_click = models.IntegerField(default=0, null=True, blank=True)
    tedad_click_shode = models.IntegerField(default=0, null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)
    vazeyat = models.CharField(max_length=10, choices=VAZEYAT_CHOICES)

    def __str__(self):
        return self.onvan


class Click(Model):
    code_tabligh = models.ForeignKey(Tabligh, on_delete=models.CASCADE)
    code_montasher_konande = models.ForeignKey(User, on_delete=models.CASCADE)
    tarikh_click = models.DateTimeField(default=datetime.now, null=True, blank=True)
    ip = models.CharField(max_length=15, null=True, blank=True)


class Payam(Model):
    code_ferestande = models.CharField(max_length=30, unique=True)
    code_girande = models.CharField(max_length=30, unique=True)
    onvan = models.CharField(max_length=30, unique=True)
    text = models.TextField(max_length=255, null=True, blank=True)
    tarikh = models.DateTimeField(default=datetime.now, null=True, blank=True)


class TanzimatPaye(Model):
    onvan = models.CharField(max_length=30, unique=True)
    value = models.CharField(max_length=10, null=True, blank=True)


if not settings.CREATING_SUPER_USER:
    @receiver(pre_save, sender=User)
    def set_new_user_inactive(sender, instance, **kwargs):
        if instance._state.adding is True:
            instance.password = make_password(instance.password)
