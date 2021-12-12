import decimal
import time
from datetime import datetime

from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from analytics.models import Rating, Cluster
from books.models import Book, Tag, TagBook
from collector.models import Log
from recommender.models import SeededRecs, Similarity

from gensim import models


def user(request, user_id):
    user_ratings = Rating.objects.filter(user_id=user_id).order_by('-rating')

    books = Book.objects.filter(pk__in=user_ratings.values('book_id'))
    log = Log.objects.filter(user_id=user_id).order_by('-created').values()[:20]

    cluster = Cluster.objects.filter(user_id=user_id).first()
    ratings = {r.book_id for r in user_ratings}

    book_dtos = list()
    sum_rating = 0
    if len(ratings) > 0:
        sum_of_ratings = sum([r.rating for r in ratings.values()])
        user_avg = sum_of_ratings/decimal.Decimal(len(ratings))
    else:
        user_avg = 0

    tags_ratings = {t['name']: 0 for t in Tag.objects.all().values('name').distinct()}
    tags_count = {t['name']: 0 for t in Tag.objects.all().values('name').distinct()}

    for book in books:
        id = book.id

        rating = ratings[id]

        r = rating.rating
        sum_rating += r
        book_dtos.append(BookDto(id, book.title, r))
        tag_book_ids = TagBook.objects.filter(book_id=id).values('tag')
        tags = Tag.objects.filter(pk__in=tag_book_ids).all()
        for tag in tags:
            if tag.name in tags_ratings.keys():
                tags_ratings[tag.name] += r - user_avg
                tags_count[tag.name] += 1

        max_value = max(tags_ratings.values())
        max_value = max(max_value, 1)
        max_count = max(tags_count.values())
        max_count = max(max_count, 1)

        tags = []
        for key, value in tags_ratings.items():
            tags.append(key, 'rating', value/max_value)
            tags.append(key, 'count', tags_count/max_count)

        cluster_id = cluster.cluster_id if cluster else 'Not in cluster'

        context_dict = {
            'user_id': user_id,
            'avg_rating': user_avg,
            'book_count': len(ratings),
            'books': sorted(book_dtos, key=lambda item: -float(item.rating))[:15],
            'tags': tags,
            'logs': list(log),
            'cluster': cluster_id,
        }

        print(tags)
        return Response(context_dict)


def content(request, content_id):
    print(content_id)
    book = Book.objects.filter(id=content_id).first()
    user_ratings = Rating.objects.filter(book_id=content_id)
    ratings = user_ratings.values('rating')
    logs = Log.objects.filter(content_id=content_id).order_by('-created').values()[:20]
    association_rules = SeededRecs.objects.filter(source=content_id).values('target', 'type')

    print(content_id, " rat:", ratings)

    book_title = 'No Title'
    agv_rating = 0
    tag_names = []
    if book is not None:
        tag_book_ids = TagBook.objects.filter(book=book).values('tag')
        tag = Tag.objects.filter(pk__in=tag_book_ids).all()
        book_tags = tag if book is not None else []
        tag_names = list(book_tags.values('name'))

        ratings = list(r['rating'] for r in ratings)
        agv_rating = sum(ratings)/len(ratings)
        book_title = book.title

    context_dict = {
        'title': book_title,
        'avg_rating': "{:10.2f}".format(agv_rating),
        'tags': tag_names,
        'association_rules': association_rules,
        'content_id': str(content_id),
        'rated_by': user_ratings,
        'logs': logs,
        'number_users': len(ratings)
    }

    return Response(context_dict)


def lda(request):
    lda = models.ldamodel.LdaModel.load('./lda/model.lda')

    for topic in lda.print_topics():
        print("topic {}: {}".format(topic[0], topic[1]))

    context_dict = {
        "topics": lda.print_topics(),
        "number_of_topics": lda.num_topics
    }

    return Response(context_dict)


def cluster(request, cluster_id):
    members = Cluster.objects.filter(cluster_id=cluster_id)
    member_ratings = Rating.objects.filter(user_id__in=members.values('user_id'))
    books = Book.objects.filter(pk__in=member_ratings.values('book_id'))

    ratings = {r.book_id: r for r in member_ratings}

    sum_rating = 0

    tags = {t['name']: 0 for t in Tag.objects.all().values('name').distinct()}
    for book in books:
        id = book.id
        rating = ratings[id]

        r = rating.rating
        sum_rating += r
        tag_book_ids = TagBook.objects.filter(book=book).values('tag')
        tag_ids = Tag.objects.filter(pk__in=tag_book_ids).all()
        for tag in tag_ids:
            if tag.name in tags.keys():
                tags[tag.name] += r

        max_value = max(tags.values())
        tags = {key: value / max_value for key, value in tags.items()}

        context_dict = {
            'tags': tags,
            'members': sorted(m.user_id for m in members),
            'cluster_id': cluster_id,
            'member_count': len(members),
        }

        return Response(context_dict)


class BookDto(object):
    def __init__(self, id, title, rating):
        self.id = id
        self.title = title
        self.rating = rating


def top_content(request):
    cursor = connection.cursor()
    cursor.execute('SELECT \
                            content_id,\
                            mov.title,\
                            count(*) as sold\
                        FROM    collector_log log\
                        JOIN    weboo mov ON CAST(log.content_id AS INTEGER) = CAST(mov.book_id AS INTEGER)\
                        WHERE 	event like \'buy\' \
                        GROUP BY content_id, mov.title \
                        ORDER BY sold desc \
                        LIMIT 10 \
            ')

    data = dictfetchall(cursor)
    return JsonResponse(data, safe=False)


def clsuters(request):

    clusters_w_membercount = (Cluster.objects.values('cluster_id').annotate(member_count=Count('user_id')).order_by('cluster_id'))

    context_dict = {
        'cluster': list(clusters_w_membercount)
    }
    return JsonResponse(context_dict, safe=False)


def similarity_graph(request):
    sim = Similarity.objects.all()[:10000]
    source_set = [s.source for s in sim]
    nodes = [{"id":s, "label": s} for s in set(source_set)]
    edges = [{"from":s.source, "to": s.target} for s in sim]

    print(nodes)
    print(edges)

    context_dict = {
        "nodes": nodes,
        "edges": edges
    }

    return Response(context_dict)


def get_statistics(request):
    date_timestamp = time.strptime(request.GET["date"], "%Y-%m-%d")

    end_date = datetime.fromtimestamp(time.mktime(date_timestamp))

    start_date = monthdelta(end_date, -1)
    print("getting statics for", start_date, " end", end_date)

    sessions_with_conversions = Log.objects.filter(created__range=(start_date, end_date), event='buy') \
        .values('session_id').distinct()
    read_data = Log.objects.filter(created__range=(start_date, end_date), event='read') \
        .values('event', 'user_id', 'content_id', 'session_id')
    visitors = Log.objects.filter(created__range=(start_date, end_date)) \
        .values('user_id').distinct()
    sessions = Log.objects.filter(created__range=(start_date, end_date)) \
        .values('session_id').distinct()

    if len(sessions) == 0:
        conversions = 0
    else:
        conversions = (len(sessions_with_conversions) / len(sessions)) * 100
        conversions = round(conversions)

    return JsonResponse(
        {
            "items_read": len(read_data),
            "conversions": conversions,
            "visitors:": len(visitors),
            "sessions": len(sessions)
        }
    )


def events_on_conversions(request):
    cursor = connection.cursor()
    cursor.execute('''select
                                (case when c.conversion = 1 then \'Read\' else \'No read\' end) as conversion,
                                event,
                                    count(*) as count_items
                                  FROM
                                        collector_log log
                                  LEFT JOIN
                                    (SELECT session_id, 1 as conversion
                                     FROM   collector_log
                                     WHERE  event=\'read\') c
                                     ON     log.session_id = c.session_id
                                   GROUP BY conversion, event''')
    data = dictfetchall(cursor)
    print(data)

    return JsonResponse(data, safe=False)


def ratings_distribution(request):
    cursor = connection.cursor()
    cursor.execute("""
        select rating, count(1) as count_items
        from analytics_rating
        group by rating
        order by rating
        """)
    data = dictfetchall(cursor)
    for d in data:
        d['rating'] = round(d['rating'])

    return JsonResponse(data, safe=False)


def monthdelta(date, delta):
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m: m = 12
    d = min(date.day, [31,
                       29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date.replace(day=d, month=m, year=y)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class book_rating():
    title = ""
    rating = 0

    def __init__(self, title, rating):
        self.title = title
        self.rating = rating

