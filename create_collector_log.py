import os

import csv
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

import django

django.setup()

from collector.models import Log


#
#
# def read_csv_logs(URL):
#     with open(URL, encoding="unicode_escape") as csv_file:
#         reader = csv.reader(csv_file)
#         for row in reader:
#             created = row[0]
#             user_id = row[1]
#             content_id = row[2]
#             event = row[3]
#             session_id = row[4]
#             collector = Log.objects.create(created=created, user_id=user_id, content_id=content_id, event=event,
#                                            session_id=session_id)
#             collector.save()
#             print("finished read csv")
#
#
# def delete_db():
#     print('truncate db')
#     collector_count = Log.objects.all().count()
#
#     if collector_count > 0:
#         Log.objects.all().delete()
#     print('finished truncate db')
#
#
def populate():
    # read_csv_logs("C:\\Users\\linhn\\OneDrive\\Documents\\csv\\collector_log.csv")
    events = ['read', 'like', 'details']
    x = range(2, 17541)
    for i in x:
        # content_id = random.randrange(1, 19126)
        user_id = i
        content_id = 1
        event = random.choice(events)
        session_id = "ed292862-5776-11ec-8759-f3d8e1eac89a"
        created = "2021-12-08 06:01:32.464787"

        log = Log.objects.create(content_id=content_id, user_id=user_id, event=event, session_id=session_id,
                                 created=created)
        log.save()


if __name__ == '__main__':
    print("Starting Collector Log script...")
    # delete_db()
    populate()
