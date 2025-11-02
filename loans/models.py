from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    age = models.IntegerField(default=0)
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField()
    current_debt = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id})"

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")
    loan_amount = models.FloatField()
    tenure = models.IntegerField(help_text="tenure in months")
    interest_rate = models.FloatField(help_text="Annual interest rate in percent")
    monthly_installment = models.FloatField()
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date and self.start_date:
            self.end_date = self.start_date + relativedelta(months=self.tenure)
        super().save(*args, **kwargs)

    @property
    def months_elapsed(self):
        if not self.start_date:
            return 0
        today = timezone.now().date()
        months = (today.year - self.start_date.year) * 12 + (today.month - self.start_date.month)
        return max(0, min(self.tenure, months))

    @property
    def repayments_left(self):
        return max(0, self.tenure - self.months_elapsed)
