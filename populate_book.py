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
# from books.models import Book, TagBook, Tag
#
#
# def create_movie(movie_id, title, genres):
#     movie = Book.objects.get_or_create(movie_id=movie_id)[0]
#
#     title_and_year = title.split(sep="(")
#
#     movie.title = title_and_year[0]
#     movie.year = title_and_year[1][:-1]
#
#     # if genres:
#     #     for genre in genres.split(sep="|"):
#     #         g = Genre.objects.get_or_create(name=genre)[0]
#     #         movie.genres.add(g)
#     #         g.save()
#
#     movie.save()
#
#     return movie
#
#
# def read_csv_books(URL):
#     with open(URL, encoding="unicode_escape") as csv_file:
#         reader = csv.reader(csv_file)
#         for row in reader:
#             book_id = row[0]
#             title = row[1]
#             description = "5 năm trước, Nguyễn Chỉ và đối tượng thầm mến Kì Trạm chia tay nhau trong hoàn cảnh không vui." \
#                           " Hiện tại 5 năm sau, anh lại bất ngờ xuất hiện trong cuộc sống của cô... " \
#                           "Nam thần, không phải anh học kiến trúc sau? Sao lại trở thành ông chủ công ty phối âm? Cái gì?" \
#                           " Đại thần CV mà cô ngưỡm mộ lại là anh sao? Thật lâu về sau khi bị Kì Trạm ăn hết sạch, Nguyễn Chỉ thầm oán, nam thần giấu kĩ thật." \
#                           " Toàn bộ nội dung do A Ke Wen Hua Official đăng tải. Đó là quan điểm và quyền quyết định của người đăng tải, không thể hiện lập trường của Weeboo."
#             book = Book.objects.create(id=book_id, title=title, description=description, author="SONA Comic")
#             book.save
#             tag = row[2]
#             tag_book = TagBook.objects.create(tag_id=tag, book=book)
#             tag_book.save()
#             print("finished read csv")
#
#
# def delete_db():
#     print('truncate db')
#     book_count = Book.objects.all().count()
#
#     if book_count > 0:
#         Book.objects.all().delete()
#         TagBook.objects.all().delete()
#     print('finished truncate db')
#
#
# def populate():
#     read_csv_books("C:\\Users\\linhn\\OneDrive\\Documents\\csv\\moviegeeks_movie.csv")
#
#
# if __name__ == '__main__':
#     print("Starting MovieGeeks Population script...")
#     delete_db()
#     populate()