import os

import csv
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

import django

django.setup()

from posts.models import PostGroup
from apps.vadmin.permission.models import UserProfile
from groups.models import Group
from books.models import Comment, Reply, Book, Chapter


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
    contents = [
        'Làm nv kiếm p xem truyện',
        'chap ngắn :<<<',
        'Na9 kểu :)) ta tưởng đâu ăn kểu kia (wao...) anh nhà tui có 1 cái đầu trong sáng ghê toa',
        'Cmt vì nhiệm vụ(◠‿◠)',
        'Mik chỉ lm nv thôi mn đừng qt ( ai muốn lm nv thì vào tl bl của mik nha',
        'Làm nv',
        'Mình lam nv bha',
        'Làm việc quan trọng zữ',
        'Nư9 ăn mặc giản dị qué',
        'S lại người đàn bà, người phụ nữ nghe hay hơn',
        'Truyện này hay k',
        'Đang làm nv không cần để ý',
        'Ms vô đã thấy vừa mắt r^^',
        'Làm nv kiếm p xem truyện',
        'Muốn đọc mà lười bình luận quá',
        'Bình luận đầu tiên',
        'Tuyệt',
        'Ơ chỉ hút thui mà sao cởi áo',
        'Very good',
        'Lol ba chung may',
        'Dit me chung may',
        'To tong chung may'
    ]
    # x = range(1, 19126)
    # for i in x:
    #     user = UserProfile.objects.filter(pk=i).first()
    #     if user is None:
    #         user_id = random.choice(UserProfile.objects.all().values_list('id'))
    #         book = Book.objects.filter(pk=i).first()
    #         content = random.choice(contents)
    #         like_count = random.randint(4, 2765)
    #
    #         comment_book = Comment.objects.create(book=book, user_id=user_id[0], content=content, like_count=like_count)
    #         comment_book.save()
    #     else:
    #         user_id = user.id
    #         book = Book.objects.filter(pk=i).first()
    #         content = random.choice(contents)
    #         like_count = random.randint(4, 2765)
    #
    #         comment_book = Comment.objects.create(book=book, user_id=user_id, content=content, like_count=like_count)
    #         comment_book.save()

    books = Book.objects.filter().values_list('id')
    for i in books:
        users = UserProfile.objects.filter(pk=random.randint(1, 19126)).first()
        book = Book.objects.filter(pk=i[0]).first()
        chapter = Chapter.objects.filter(book_id=book.id).first()
        if users is None:
            user = 2
        else:
            user = users.id
        if chapter is None:
            chapter_id = Chapter.objects.filter(pk=2).first()
            content = random.choice(contents)
            like_count = random.randint(4, 2765)
            comment_book = Comment.objects.create(book=book, user_id=user, chapter=chapter_id, content=content, like_count=like_count)
            comment_book.save()
        else:
            content = random.choice(contents)
            like_count = random.randint(4, 2765)

            comment_book = Comment.objects.create(book=book, user_id=user, chapter_id=chapter.id, content=content,
                                                  like_count=like_count)
            comment_book.save()

        user_id = random.choice(UserProfile.objects.all().values_list('id'))
        reply = random.choice(contents)
        like_count = random.randint(0, 123)
        reply = Reply.objects.create(comment_id=comment_book.id, user_id=user_id[0], reply=reply, like_count=like_count)
        reply.save()


if __name__ == '__main__':
    print("Starting create comment script...")
    # delete_db()
    populate()
