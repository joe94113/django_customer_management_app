# https://docs.djangoproject.com/en/3.0/topics/signals/
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer


def customer_profile(sender, instance, created, **krgs):
    if created:
        group = Group.objects.get(name="customer")
        instance.groups.add(group)  # 新建立用戶自動加入group = customer

        Customer.objects.create(
            user=instance,
            name=instance.username,
        )
        print('Profile Created')


post_save.connect(customer_profile, sender=User)
