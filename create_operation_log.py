import os

# import csv
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')

import django

django.setup()

from builtins import str
from posts.models import PostGroup
from django.contrib.auth import get_user_model
from apps.vadmin.system.models import OperationLog

from collector.models import Log
from apps.vadmin.permission.models import UserProfile, Role

# from django.contrib.auth.models import User

User = get_user_model()


def populate():
    # read_csv_logs()
    # create_datetime = "2021-12-16 20:58:25.660251"
    # update_datetime = "2021-12-16 20:58:25.660251"
    # request_path = "/login"
    # request_body = "{'username': 'quyennguyen@gmail.com', 'password': '********'}"
    # request_method = "POST"
    # request_ip = "127.0.0.1"
    # request_browser = "Other"
    # request_os = "Other"
    # json_result = "{'code': None, 'msg': None}"
    #
    # x = range(1, 34572)
    # for i in x:
    #     operator = OperationLog.objects.create(create_datetime=create_datetime, update_datetime=update_datetime,
    #                                        request_path=request_path, request_body=request_body,
    #                                        request_method=request_method, request_ip=request_ip,
    #                                        request_browser=request_browser, request_os=request_os,
    #                                        json_result=json_result)
    #     operator.save()
    list_image = ["/media/books/2021/12/18/download.jpeg", "/media/books/2021/12/18/wp9392827.jpeg",
                  "/media/books/2021/12/18/iu-lovepoem-1.jpeg", "/media/books/2021/12/18/saostar-q3nn9pfsydf1uhvk.jpeg"]

    post_group = PostGroup.objects.filter()
    for i in post_group:
        i.image_url = random.choice(list_image)
        i.save()
        print(i.id)


if __name__ == '__main__':
    print("Starting create login script...")
    populate()
