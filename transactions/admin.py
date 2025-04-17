# transactions/admin.py

from django.contrib import admin
from .models import Transaction, Installment, Notification

class InstallmentInline(admin.TabularInline):
    model = Installment
    extra = 0

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'customer', 'product', 'total_price', 'remaining_amount', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['transaction_id', 'customer__email', 'product__name']
    inlines = [InstallmentInline]

class InstallmentAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'amount', 'due_date', 'payment_date', 'status']
    list_filter = ['status', 'due_date']
    search_fields = ['transaction__transaction_id', 'transaction__customer__email']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['installment', 'type', 'sent_date', 'is_sent']
    list_filter = ['type', 'is_sent']

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Installment, InstallmentAdmin)
admin.site.register(Notification, NotificationAdmin)