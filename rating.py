import os

import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

import django
django.setup()

from analytics.models import Rating


def read_csv_books(URL):
    with open(URL, encoding="unicode_escape") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            user_id = row[0]
            book_id = row[1]
            rating = float(row[2])
            rating_timestamp = row[3]
            # type = row[4]
            rating = Rating.objects.create(user_id=user_id, book_id=book_id, rating=rating, rating_timestamp=rating_timestamp, type=type)
            rating.save
            print(row)


def delete_db():
    print('truncate db')
    rating = Rating.objects.all().count()

    if rating > 0:
        Rating.objects.all().delete()
    print('finished truncate db')


def populate():
    read_csv_books("C:\\Users\\linhn\\OneDrive\\Documents\\csv\\ratings.csv")


if __name__ == '__main__':
    print("Starting rating Population script...")
    # delete_db()
    populate()