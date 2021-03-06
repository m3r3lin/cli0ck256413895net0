from django.contrib import admin
from system.models import TicketMessages, User, Pelan, Tabligh, Click, Payam, TanzimatPaye, KifPool, TablighatMontasherKonande, Role, SoodeTabligh, HistoryIndirect, KifDarAmad


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
    list_display = ('id', 'tabligh', 'montasher_konande', 'tarikh', 'ip',)
    # list_display = [field.attname for field in Tabligh._meta.fields]


class PayamAdmin(admin.ModelAdmin):
    list_display = ('id', 'ferestande', 'girande', 'onvan', 'tarikh', 'text',)
    # list_display = [field.attname for field in Tabligh._meta.fields]


class KifePoolAdmin(admin.ModelAdmin):
    pass


class TablighatMontasherKonandeAdmin(admin.ModelAdmin):
    pass


class SoodeTablighAdmin(admin.ModelAdmin):
    pass


class HistoryIndirectAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Pelan, PelanAdmin)
admin.site.register(Tabligh, TablighAdmin)
admin.site.register(Click, ClickAdmin)
admin.site.register(Payam, PayamAdmin)
admin.site.register(TanzimatPaye)
admin.site.register(Role)
admin.site.register(KifPool, KifePoolAdmin)
admin.site.register(TablighatMontasherKonande, TablighatMontasherKonandeAdmin)
admin.site.register(SoodeTabligh, SoodeTablighAdmin)
admin.site.register(HistoryIndirect, HistoryIndirectAdmin)
admin.site.register(KifDarAmad)
admin.site.register(TicketMessages)
