from django.contrib import admin

from .models import Payment


# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('value', 'currency', 'description')


admin.site.register(Payment, PaymentAdmin)
