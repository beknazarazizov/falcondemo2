from django.contrib import admin
from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin

from app.models import Product, Image, Attribute, AttributeValue, ProductAttribute

# Register your models here.


# admin.site.register(Product)
# admin.site.register(Image)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)

# admin.site.unregister(User)
admin.site.unregister(Group)


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'price')


# admin.site.register(Product, ProductModelAdmin)


@admin.register(Product)
class ProductModelAdmin(SortableAdminMixin, ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'rating', 'quantity']
    search_fields = ['name', 'price', 'rating']
    list_filter = ['price', 'rating']


@admin.register(Image)
class ImagesModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'image', 'product']
    search_fields = ['product']
