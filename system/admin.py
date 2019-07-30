from django.contrib import admin
from system.models import User, Pelan, Tabligh, Click, Payam


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'code_melli', 'first_name', 'last_name', 'gender',)
    # list_display = [field.attname for field in User._meta.fields]


class PelanAdmin(admin.ModelAdmin):
    list_display = ('id', 'onvan', 'gheymat', 'tarikh_ijad', 'vazeyat',)
    # list_display = [field.attname for field in Pelan._meta.fields]


class TablighAdmin(admin.ModelAdmin):
    list_display = ('id', 'onvan', 'code_tabligh_gozaar', 'tarikh_ijad', 'code_pelan',)
    # list_display = [field.attname for field in Tabligh._meta.fields]


class ClickAdmin(admin.ModelAdmin):
    list_display = ('id', 'code_tabligh', 'code_montasher_konande', 'tarikh_click', 'ip',)
    # list_display = [field.attname for field in Tabligh._meta.fields]


class PayamAdmin(admin.ModelAdmin):
    list_display = ('id', 'code_ferestande', 'code_girande', 'onvan', 'tarikh', 'text',)
    # list_display = [field.attname for field in Tabligh._meta.fields]


admin.site.register(User, UserAdmin)
admin.site.register(Pelan, PelanAdmin)
admin.site.register(Tabligh, TablighAdmin)
admin.site.register(Click, ClickAdmin)
admin.site.register(Payam, PayamAdmin)
