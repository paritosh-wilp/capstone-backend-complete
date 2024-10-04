from django.contrib import admin

# Register your models here.

from .models import Business
from .models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('business', 'session_date', 'timeslot', 'session_status', 'customer')
    list_filter = ('session_status', 'session_date', 'business')
    search_fields = ('business__business_name', 'customer__customer_name')

