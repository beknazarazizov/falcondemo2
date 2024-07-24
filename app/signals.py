import json
import os

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from app.models import Product
from falcondemo.settings import BASE_DIR


@receiver(post_save, sender=Product)
def product_post_save(sender, instance,created, **kwargs):
    if created:
        print(f"{instance.name} created!")

    else:
        print(f"{instance.name} updated!")

# @receiver(pri_delete, sender=Product)
# def product_post_delete(sender, instance,deleted, **kwargs):
#     if deleted:
#         with open("Product.json", "w") as f:
#             f.write(instance.objects.all())
#             print(f"{instance.name} deleted!")



@receiver(pre_delete, sender=Product)
def product_delete(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'app/delete_products/', f'product_{instance.id}.json')


    product_data = {
        'id': instance.id,
        'name': instance.name,
        'price': instance.price,
        'description': instance.description
    }

    with open( file_path, mode='w') as file_json:
        json.dump(product_data, file_json, indent=4)

    print(f'{instance.name} is deleted')