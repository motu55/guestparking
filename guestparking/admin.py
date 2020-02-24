from django.contrib import admin

from guestparking.models import Car, Flat


class DefaultAdmin(admin.ModelAdmin):
    pass


admin.site.register(Car, DefaultAdmin)
admin.site.register(Flat, DefaultAdmin)