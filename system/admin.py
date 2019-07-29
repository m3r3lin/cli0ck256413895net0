from django.contrib import admin
from system.models import User, Pelan


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'code_melli', 'first_name', 'last_name', 'gender',)
    # list_display = [field.attname for field in User._meta.fields]


class PelanAdmin(admin.ModelAdmin):
    list_display = ('code_pelan', 'onvan', 'gheymat', 'tarikh_ijad', 'vazeyat',)
    # list_display = [field.attname for field in Pelan._meta.fields]


admin.site.register(User, UserAdmin)
admin.site.register(Pelan, PelanAdmin)
