from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from app.models import Product
from customer.forms import UserModelForm
from customer.models import Customer, User

# Register your models here.
# admin.site.register(Customer)



@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email']
    search_fields = ['email', 'id']
    list_filter = ['joined', 'full_name']
    list_per_page = 5

    def has_add_permission(self, request):
        return True

    def has_view_or_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'birth_of_date', 'is_superuser']
    form=UserModelForm

