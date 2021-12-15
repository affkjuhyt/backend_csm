# import os
#
# import csv
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
#
# import django
#
# django.setup()
#
# from collector.models import Log
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
# def populate():
#     read_csv_logs("C:\\Users\\linhn\\OneDrive\\Documents\\csv\\collector_log.csv")
#
#
# if __name__ == '__main__':
#     print("Starting Collector Log script...")
#     delete_db()
#     populate()
