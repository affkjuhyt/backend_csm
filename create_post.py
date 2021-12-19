import os

import csv
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

import django

django.setup()

from posts.models import PostGroup
from apps.vadmin.permission.models import UserProfile
from groups.models import Group

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
        'As plague and turmoil afflicts the empire, enchanting widow Rieta Tristi finds herself at the mercy of a malicious nobleman and his dying wish to have her buried alive beside his corpse. The plague has taken her husband, slave traders have taken her young child, and now her own life is at risk',
        'What happens when a struggling witch meets an angsty vampire? Either love or war. Morgana belongs to a long line of witches, and Oz to the rival vampire clan. After a chance encounter… and maybe a few stray spells… these two need to find a way to work together, or risk all-out war between coven and clan.',
        'She’s young, single and about to achieve her dream of creating incredible videogames. But then life throws her a one-two punch: a popular streamer gives her first game a scathing review. Even worse she finds out that same troublesome critic is now her new neighbor! A funny, sexy and all-too-real story about gaming, memes and social anxiety. Come for the plot, stay for the doggo.']
    x = range(2, 17541)
    for i in x:
        # content_id = random.randrange(1, 19126)
        user = UserProfile.objects.filter(pk=i).first()
        if user is None:
            user_id = 2
            group_id = Group.objects.filter(pk=random.randrange(1, 8, 1)).first().id
            content = random.choice(contents)
            image_url = "http://127.0.0.1:8000/media/books/2021/12/17/1615000386688.5897_vwSHw0P.jpg"

            post = PostGroup.objects.create(user_id=user_id, group_id=group_id, content=content, image_url=image_url)
            post.save()
        else:
            user_id = user.id
            group_id = Group.objects.filter(pk=random.randrange(1, 8, 1)).first().id
            content = random.choice(contents)
            image_url = "http://127.0.0.1:8000/media/books/2021/12/17/1615000386688.5897_vwSHw0P.jpg"

            post = PostGroup.objects.create(user_id=user_id, group_id=group_id, content=content, image_url=image_url)
            post.save()


if __name__ == '__main__':
    print("Starting create post script...")
    # delete_db()
    populate()
