from asynchat import simple_producer

from django.shortcuts import render

# Create your views here.
import operator
from decimal import Decimal
from math import sqrt

import numpy as np
from django.db.models import Avg, Count
from django.http import JsonResponse
from rest_framework.decorators import api_view

from analytics.models import Rating
from apps.vadmin.permission.models import UserProfile
from collector.models import Log
from books.models import Book, TagBook, Tag
from recommender.models import SeededRecs
from recs.bpr_recommender import BPRRecs
from recs.content_based_recommender import ContentBasedRecs
from recs.funksvd_recommender import FunkSVDRecs
from recs.fwls_recommender import FeatureWeightedLinearStacking
from recs.neighborhood_based_recommender import NeighborhoodBasedRecs
from recs.popularity_recommender import PopularityBasedRecs


@api_view(['GET'])
def get_association_rules_for(request, content_id, take=6):
    data = SeededRecs.objects.filter(source=content_id) \
               .order_by('-confidence') \
               .values('target', 'confidence', 'support')[:take]

    return JsonResponse(dict(data=list(data)), safe=False)


@api_view(['GET'])
def recs_using_association_rules(request, user_id, take=6):
    events = Log.objects.filter(user_id=user_id)\
                        .order_by('created')\
                        .values_list('content_id', flat=True)\
                        .distinct()

    seeds = set(events[:20])

    rules = SeededRecs.objects.filter(source__in=seeds) \
        .exclude(target__in=seeds) \
        .values('target') \
        .annotate(confidence=Avg('confidence')) \
        .order_by('-confidence')

    recs = [{'id': '{0:07d}'.format(int(rule['target'])),
             'confidence': rule['confidence']} for rule in rules]

    print("recs from association rules: \n{}".format(recs[:take]))
    return JsonResponse(dict(data=list(recs[:take])))


@api_view(['GET'])
def chart(request, take=10):
    sorted_items = PopularityBasedRecs().recommend_items_from_log(take)
    ids = [i['content_id'] for i in sorted_items]

    ms = {m['id']: m['title'] for m in
          Book.objects.filter(pk__in=ids).values('title', 'id')}

    if len(ms) > 0:
        sorted_items = [{'id': i['content_id'],
                          'title': ms[i['content_id']]} for i in sorted_items]
    else:
        print("No data for chart found. This can either be because of missing data, or missing book data")
        sorted_items = []
    data = {
        'data': sorted_items
    }

    return JsonResponse(data, safe=False)


def pearson(users, this_user, that_user):
    if this_user in users and that_user in users:
        this_user_avg = sum(users[this_user].values()) / len(users[this_user].values())
        that_user_avg = sum(users[that_user].values()) / len(users[that_user].values())

        all_books = set(users[this_user].keys()) & set(users[that_user].keys())

        dividend = 0
        a_divisor = 0
        b_divisor = 0
        for book in all_books:

            if book in users[this_user].keys() and book in users[that_user].keys():
                a_nr = users[this_user][book] - this_user_avg
                b_nr = users[that_user][book] - that_user_avg
                dividend += a_nr * b_nr
                a_divisor += pow(a_nr, 2)
                b_divisor += pow(b_nr, 2)

        divisor = Decimal(sqrt(a_divisor) * sqrt(b_divisor))
        if divisor != 0:
            return dividend / Decimal(sqrt(a_divisor) * sqrt(b_divisor))

    return 0


def jaccard(users, this_user, that_user):
    if this_user in users and that_user in users:
        intersect = set(users[this_user].keys()) & set(users[that_user].keys())

        union = set(users[this_user].keys()) | set(users[that_user].keys())

        return len(intersect) / Decimal(len(union))
    else:
        return 0


@api_view(['GET'])
def similar_users(request, user_id, sim_method):
    min = request.GET.get('min', 1)

    ratings = Rating.objects.filter(user_id=user_id)
    sim_users = Rating.objects.filter(book_id__in=ratings.values('book_id')) \
        .values('user_id') \
        .annotate(intersect=Count('user_id')).filter(intersect__gt=min)

    dataset = Rating.objects.filter(user_id__in=sim_users.values('user_id'))

    users = {u['user_id']: {} for u in sim_users}

    for row in dataset:
        if row.user_id in users.keys():
            users[row.user_id][row.book_id] = row.rating

    similarity = dict()

    switcher = {
        'jaccard': jaccard,
        'pearson': pearson,

    }

    for user in sim_users:
        func = switcher.get(sim_method, lambda: "nothing")
        s = func(users, user_id, user['user_id'])

        if s > 0.2:
            similarity[user['user_id']] = round(s, 2)

    topn = sorted(similarity.items(), key=operator.itemgetter(1), reverse=True)[:15]
    # key = similarity.keys()
    list = []

    for i in similarity.keys():
        key = {}
        user = UserProfile.objects.filter(pk=i).first()
        if user is None:
            user = UserProfile.objects.filter(pk=2).first()
        key['username'] = user.username
        key['group'] = user.groups.name
        key['gender'] = user.gender
        list.append(key)

    data = {
        'user_id': user_id,
        'num_books_rated': len(ratings),
        'type': sim_method,
        'similarity': list,
    }

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def similar_content(request, content_id, num=6):

    sorted_items = ContentBasedRecs().seeded_rec([content_id], num)

    list = []
    for i in sorted_items:
        key = {}
        book = Book.objects.filter(pk=i['target']).first()
        key['book_id'] = book.id
        key['book_name'] = book.title
        key['author'] = book.author
        tag_book = TagBook.objects.filter(book=book).values('id')
        tag = Tag.objects.filter(pk__in=tag_book)
        if len(tag) == 0:
            key['book_tag'] = ""
        else:
            key['book_tag'] = tag.values('name')
        list.append(key)

    data = {
        'source_id': content_id,
        'data': list
    }

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def recs_cb(request, user_id, num=6):

    sorted_items = ContentBasedRecs().recommend_items(user_id, num)

    list = []
    for i in sorted_items:
        key = {}
        key['book_id'] = i[0]
        book = Book.objects.filter(pk=i[0]).first()
        key['book_name'] = book.title
        key['count_book_similarity'] = i[1]['sim_items'][0]
        key['point_similarity'] = i[1]['prediction']
        key['author'] = book.author
        tag_book = TagBook.objects.filter(book=book).values('id')
        tag = Tag.objects.filter(pk__in=tag_book)
        if len(tag) == 0:
            key['book_tag'] = ""
        else:
            key['book_tag'] = tag.values('name')
        list.append(key)

    data = {
        'user_id': user_id,
        'data': list
    }

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def recs_fwls(request, user_id, num=6):
    sorted_items = FeatureWeightedLinearStacking().recommend_items(user_id, num)

    data = {
        'user_id': user_id,
        'data': sorted_items
    }
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def recs_funksvd(request, user_id, num=6):
    sorted_items = FunkSVDRecs().recommend_items(user_id, num)

    list = []
    for i in sorted_items:
        key = {}

    data = {
        'user_id': user_id,
        'data': sorted_items
    }
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def recs_bpr(request, user_id, num=6):
    sorted_items = BPRRecs().recommend_items(user_id, num)

    list = []
    for i in sorted_items:
        key = {}
        user = UserProfile.objects.filter(pk=i[0]).first()
        key['user_id'] = user.id
        key['username'] = user.username
        key['prediction'] = i[1]['prediction']
        list.append(key)

    data = {
        'user_id': user_id,
        'data': list
    }
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def recs_cf(request, user_id, num=6):
    min_sim = request.GET.get('min_sim', 0.1)
    sorted_items = NeighborhoodBasedRecs(min_sim=min_sim).recommend_items(user_id, num)

    print(f"cf sorted_items is: {sorted_items}")
    data = {
        'user_id': user_id,
        'data': sorted_items
    }

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def recs_pop(request, user_id, num=60):
    top_num = PopularityBasedRecs().recommend_items(user_id, num)
    data = {
        'user_id': user_id,
        'data': top_num[:num]
    }

    return JsonResponse(data, safe=False)

def lda2array(lda_vector, len):
    vec = np.zeros(len)
    for coor in lda_vector:
        if coor[0] > 1270:
            print("auc")
        vec[coor[0]] = coor[1]

    return vec
