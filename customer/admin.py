from django.contrib import admin

from app.models import Product
from customer.models import Customer

# Register your models here.
# admin.site.register(Customer)



@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email']
    search_fields = ['email', 'id']
    list_filter = ['joined', 'full_name']
