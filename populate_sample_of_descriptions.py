# import csv
# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
#
# import django
#
# django.setup()
#
# from recommender.models import BookDescriptions
#
#
# def delete_db():
#     print('truncate db')
#     book_description = BookDescriptions.objects.all().count()
#
#     if book_description > 0:
#         BookDescriptions.objects.all().delete()
#     print('finished truncate db')
#
#
# def read_csv_descriptions(URL):
#     with open(URL, encoding="unicode_escape") as csv_file:
#         reader = csv.reader(csv_file)
#         for row in reader:
#             book_id = row[0]
#             title = row[2]
#             description = row[3]
#             tags = row[4]
#             lda_vector = row[5]
#             sim_list = row[6]
#             book_description = BookDescriptions.objects.create(book_id=book_id, title=title, description=description,
#                                                                tags=tags,
#                                                                lda_vector=lda_vector, sim_list=sim_list)
#             book_description.save()
#             print("finished read csv")
#
#
# def populate():
#     read_csv_descriptions("C:\\Users\\linhn\\OneDrive\\Documents\\csv\\movie_description.csv")
#
#
# if __name__ == '__main__':
#     print("Starting books population script")
#     delete_db()
#     populate()
