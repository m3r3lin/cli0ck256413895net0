import math
from datetime import timedelta

from allauth.account import signals
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Model, Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from Ads_Project import settings
from Ads_Project.settings import MAIN_ADMIN_ID
from system.functions import upload_avatar_path, upload_cart_melli_path

INCREASE_BALANCE_ORDER = 12

VAZEYAT_CHOICES = (
    (0, _('activate')),
    (1, _('deactivate')),
)
VAZEYAT_Tabligh = (
    (0, _('deactivate')),
    (1, _('activate')),
    (2, _('canceled')),
    (3, _('waiting')),
    (4, _('finished')),
)
GENDER_CHOICES = (
    (0, _("woman")),
    (1, _("man")),
    (2, _("not specified")),
)
NOOE_CHOICES = (
    (0, _("Ad Maker")),
    (1, _("Ad Publisher")),
    (2, _("Both")),
)
VAZEYAT_PAYAM = (
    (0, _('read')),
    (1, _('unread')),
    (2, _('sent')),
)


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    title = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title


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
    kife_daramad = models.FloatField(default=0, validators=[MinValueValidator(0),
                                                            MaxValueValidator(
                                                                9999999999,
                                                                message=_('Income Pocket cant be greater than 9999999999'))
                                                            ])
    code_moaref = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True)
    sath = models.IntegerField(default=1, null=True, blank=True)
    id_telegram = models.CharField(max_length=30, null=True, blank=True)
    nooe_heshab = models.IntegerField(null=True, blank=True, choices=NOOE_CHOICES)
    vazeyat = models.IntegerField(null=True, blank=True, choices=VAZEYAT_CHOICES)
    image_cart_melli = models.ImageField(upload_to=upload_cart_melli_path, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_avatar_path, null=True, blank=True)
    roles = models.ManyToManyField(Role, related_name="users", related_query_name="user", blank=True)
    list_parent = models.TextField(null=True, blank=True)
    last_logout = models.DateTimeField(blank=True, null=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    country = CountryField(null=True)

    def is_complete(self):
        if self.first_name is not None or \
                self.last_name is not None or \
                self.code_melli is not None or \
                self.tarikh_tavalod is not None or \
                self.mobile is not None or \
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

    @property
    def user_status(self):
        if self.last_activity:
            online_time_limite = timezone.now() - timedelta(seconds=1800)
            if self.last_activity >= online_time_limite:
                return True
            else:
                return False
        else:
            return False

    def get_kif_kif_pool(self) -> "KifPool":
        k, _ = KifPool.objects.get_or_create(user=self, defaults=dict(user=self))
        return k

    def add_to_kif_pool(self, adad: int):
        k = self.get_kif_kif_pool()
        k.current_balance += adad
        k.save()

    def sub_from_kif_pool(self, adad: int):
        k = self.get_kif_kif_pool()
        k.current_balance -= adad
        k.save()

    def get_kif_daramad(self) -> "KifDarAmad":
        k, _ = KifDarAmad.objects.get_or_create(user=self, defaults=dict(user=self))
        return k

    def add_to_kif_daramad(self, adad: int, direct=True):
        k = self.get_kif_daramad()
        if direct:
            k.current_recieved_direct += adad
        else:
            k.current_recieved_indirect += adad
        k.save()

    @property
    def kife_pool(self):
        return self.get_kif_kif_pool().current_balance

    def allow_indirect(self):
        allowed = TanzimatPaye.get_settings(COUNT_KHARI_HADAGHAL, 0)
        return self.tabligh_set.filter(vazeyat=1).count() >= allowed

    def __str__(self):
        return self.username

    def delete(self, using=None, keep_parents=False):
        if self.id != MAIN_ADMIN_ID:
            return super().delete(using, keep_parents)


class KifPool(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_balance = models.FloatField(default=0)
    all_received_direct = models.FloatField(default=0)
    all_received_indirect = models.FloatField(default=0)
    all_deposit = models.FloatField(default=0)
    all_received = models.FloatField(default=0)


class KifDarAmad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_recieved_direct = models.FloatField(default=0)
    current_recieved_indirect = models.FloatField(default=0)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.SmallIntegerField(choices=(
        (0, _("deposit")),
        (1, _("withdraw")),
        (2, _("Income to Pocket money")),
    ))
    meghdar = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)


class Pelan(Model):
    onvan = models.CharField(max_length=80, unique=True)
    gheymat = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    tarikh_ijad = models.DateTimeField(auto_now_add=True)
    tedad_click = models.IntegerField()
    vazeyat = models.IntegerField(choices=VAZEYAT_CHOICES)

    def __str__(self):
        return '{} - {}'.format(self.onvan, str(math.trunc(self.gheymat) if self.gheymat > 0 else '0'))


class Tabligh(Model):
    onvan = models.CharField(max_length=80)
    text = models.TextField()
    code_tabligh_gozaar = models.ForeignKey(User, on_delete=models.CASCADE)
    tarikh_ijad = models.DateTimeField(auto_now_add=True)
    code_pelan = models.ForeignKey(Pelan, on_delete=models.CASCADE)
    tedad_click = models.IntegerField()
    tedad_click_shode = models.IntegerField(default=0)
    vazeyat = models.IntegerField(choices=VAZEYAT_Tabligh)
    mablagh_har_click = models.FloatField()
    mablagh_tabligh = models.PositiveIntegerField()
    random_url = models.CharField(max_length=255)

    @property
    def show_url(self):
        return reverse('PreviewTabligh', args=[self.random_url])

    @property
    def subbed(self):
        if self.tedad_click_shode < self.tedad_click:
            return self.tedad_click - self.tedad_click_shode
        return 0

    @property
    def all_users(self):
        return TablighatMontasherKonande.objects.filter(tabligh=self)

    def __str__(self):
        return self.onvan


class Click(Model):
    tabligh = models.ForeignKey(Tabligh, on_delete=models.CASCADE)
    montasher_konande = models.ForeignKey(User, on_delete=models.CASCADE)
    mablagh_har_click = models.FloatField()
    user_agent = models.CharField(max_length=90, null=True)
    country = models.CharField(max_length=90, null=True)
    ip = models.CharField(max_length=16, null=True)
    tarikh = models.DateTimeField(auto_now_add=True)


class Payam(Model):
    ferestande = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ferestande_user_id')
    girande = models.ForeignKey(User, on_delete=models.CASCADE, related_name='girande_user_id')
    onvan = models.CharField(max_length=150)
    text = models.TextField()
    tarikh = models.DateTimeField(auto_now_add=True)
    vazeyat = models.IntegerField(choices=VAZEYAT_PAYAM)
    save_date = models.DateTimeField(default=timezone.now, blank=True, null=True)


SATH = 'sath.'
SODE_MODIR = 'sode_modir'
LANGUGE_SITE = 'languge_site'
ACTIV_MOAREF = 'active_moaref'
VAHED_POLL_SITE = 'vahed_poll_site'
TIME_KHARID_TERM = 'time_kharid_term'
TEDAD_SATH_SHABAKE = 'tedad_sath_shabake'
SHOW_AMAR_FOR_USER = 'show_amar_for_user'
COUNT_VISIT_TABLIGH = 'count_visit_tabligh'
COUNT_LEVEL_NETWORK = 'count_level_network'
TAEIN_HADAGHAL_ETBAR = 'taein_hadaghal_etbar'
COUNT_KHARI_HADAGHAL = 'count_kharid_hadaghl'
TAIEN_MEGHDAR_MATLAB = 'taien_meghdar_matlab'
TAIED_KHODKAR_TABLIGH = 'taied_khodkar_tabligh'
LEAST_BALANCE_REQUIRED = 'least_balance_required'
CLICK_IS_CHANGEABLE = 'click_is_change_able'


class TanzimatPaye(Model):
    onvan = models.CharField(max_length=250, unique=True)
    value = models.CharField(max_length=250)

    @staticmethod
    def get_settings(key, default=None):
        try:
            a = TanzimatPaye.objects.get(onvan=key).value
            if a.isdigit():
                return int(a)
            elif a.isdecimal():
                return float(a)
            return a
        except:
            return default

    def __str__(self):
        return self.onvan


class Parent(Model):
    node = models.ForeignKey(User, on_delete=models.CASCADE, related_name='node_user_id')
    parent = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='parent_user_id')


class TablighatMontasherKonande(Model):
    tabligh = models.ForeignKey(Tabligh, on_delete=models.CASCADE)
    montasher_konande = models.ForeignKey(User, models.CASCADE)
    tarikh = models.DateTimeField(auto_now_add=True)


class Order(Model):
    type = models.IntegerField(choices=(
        (INCREASE_BALANCE_ORDER, _("Increase balance")),
    ))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField(default='')


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


class HistoryIndirect(Model):
    montasher_konande = models.ForeignKey(User, on_delete=models.CASCADE, related_name="montasherkonande")
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="parent", null=True)
    mablagh = models.FloatField()
    tarikh = models.DateTimeField(auto_now_add=True)


class Infopm(Model):
    is_active = models.BooleanField(default=True)
    body = models.TextField(default='')


class SoodeTabligh(Model):
    tabligh = models.ForeignKey(Tabligh, on_delete=models.CASCADE)
    sath = models.IntegerField()
    soode_mostaghim = models.FloatField()
    soode_gheire_mostaghim = models.FloatField(default=0)
