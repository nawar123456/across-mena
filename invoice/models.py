from django.db import models

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=100)
    client_address = models.TextField()
    date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    item_description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # حساب المجموع التلقائي
        self.total = self.amount + self.tax
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number}"