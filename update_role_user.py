import os

import csv
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

import django

django.setup()

from apps.vadmin.permission.models import UserProfile, Role


def populate():
    role_vip = Role.objects.filter(id=3)
    role_common = Role.objects.filter(id=2)

    list_role = [role_vip, role_common]

    x = range(2, 17000)
    for i in x:
        try:
            user = UserProfile.objects.get(pk=i)
        except:
            user = UserProfile.objects.get(pk=2)
        user.role.add(random.choice(list_role).first().id)
        # user.role.set(random.choice(list_role))
        user.save()
        # user.entry
        print(i)


if __name__ == '__main__':
    print("Starting create comment script...")
    # delete_db()
    populate()
