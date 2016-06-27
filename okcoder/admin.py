from django.contrib import admin

# Register your models here.
from .models import Partner, Partnership, Evaluation

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'reg_date', 'consent', 'eval_complete')

class PartnershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'brief', 'complete')

class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('evaluator', 'partner')

admin.site.register(Partner, PartnerAdmin)
admin.site.register(Partnership, PartnershipAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
