# transactions/models.py

from django.db import models
from accounts.models import CustomUser
from products.models import Product
from django.utils import timezone
import uuid

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    down_payment = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.customer.email}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only calculate on creation
            self.remaining_amount = self.total_price - self.down_payment
        super().save(*args, **kwargs)

class Installment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    )
    
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='installments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Installment for {self.transaction.transaction_id} - Due: {self.due_date}"
    
    def is_overdue(self):
        return self.status == 'pending' and self.due_date < timezone.now().date()

class Notification(models.Model):
    TYPE_CHOICES = (
        ('due_date', 'Due Date Reminder'),
        ('payment', 'Payment Confirmation'),
        ('overdue', 'Overdue Payment'),
    )
    
    installment = models.ForeignKey(Installment, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    sent_date = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_type_display()} for {self.installment.transaction.customer.email}"