from django.contrib import admin

# Register your models here.
from .models import Partner

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_date', 'brief', 'consent')

admin.site.register(Partner, PartnerAdmin)
