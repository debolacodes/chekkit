from django.contrib import admin

# Register your models here.
from ussd.models import UssdData


class UssdRecordAdmin(admin.ModelAdmin):
    pass


admin.site.register(UssdData, UssdRecordAdmin)
