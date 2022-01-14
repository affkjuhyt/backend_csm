import os

# import csv
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

import django

django.setup()

from builtins import str
from django.contrib.auth import get_user_model

from collector.models import Log
from books.models import Book
from apps.vadmin.permission.models import UserProfile, Role

# from django.contrib.auth.models import User

User = get_user_model()


def read_csv_logs():
    count = range(2742, 17542)
    for n in count:
        email = "account_test" + str(n) + "@gmail.com"
        creator = UserProfile.objects.filter(pk=1).first()
        username = "account_test" + str(n)
        secret = "17aa6a04-bceb-431e-ab7e-df7a07f76a8d"
        name = "account_test" + str(n)
        remark = "remark"
        role = Role.objects.filter(pk=2).first()
        password = "123456a@"
        user = User()
        user.last_name = username
        user.username = username
        user.email = email
        user.password = password
        # user.sec
        user.creator = creator
        user.name = name
        user.remark = remark
        # user.role = role
        user.save()
        print("finished read csv")


def delete_db():
    print('truncate db')
    collector_count = Log.objects.all().count()

    if collector_count > 0:
        Log.objects.all().delete()
    print('finished truncate db')


def populate():
    # Get all book
    list_images = ["books/2022/01/11/photo_2022-01-07_21-53-53.jpg", "books/2022/01/11/photo_2022-01-07_21-54-00.jpg",
                   "books/2022/01/11/photo_2022-01-07_21-53-57_jL4Ocmh.jpg",
                   "books/2022/01/11/photo_2022-01-07_21-54-03.jpg", "books/2022/01/11/photo_2022-01-07_21-54-06.jpg"]
    books = Book.objects.filter()
    for book in books:
        book.thumbnail = random.choice(list_images)
        book.save()


if __name__ == '__main__':
    print("Starting create user script...")
    populate()
