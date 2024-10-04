from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from datetime import date

class Business(models.Model):
    business_id = models.PositiveIntegerField(unique=True) #parichan : This must be true 
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(
        max_length=50, 
        choices=(
            ("Hospital", "Hospital"),
            ("Saloon", "Saloon"),
            ("Restaurant", "Restaurant"),
        )
    )
    business_mail = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254)  # We will hash this password

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.business_name


class Customer(models.Model):
    customer_id = models.PositiveIntegerField(unique=True)
    customer_name = models.CharField(max_length=100)
    customer_mail = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.customer_name



from django.db import models
from datetime import date

class Session(models.Model):
    SESSION_STATUS_CHOICES = (
        ("isAvailable", "isAvailable"),
        ("isBooked", "isBooked"),
        ("isCancelled", "isCancelled"),
        ("isCompleted", "isCompleted"),
    )

    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    session_date = models.DateField()
    timeslot = models.CharField(max_length=100)
    session_status = models.CharField(max_length=100, choices=SESSION_STATUS_CHOICES, default="isAvailable")
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.business.business_name} - {self.session_date} - {self.timeslot} - {self.session_status}"



