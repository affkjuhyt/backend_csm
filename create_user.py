# import os
#
# # import csv
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
#
# import django
#
# django.setup()
#
# from builtins import str
# from django.contrib.auth import get_user_model
#
# from collector.models import Log
# from apps.vadmin.permission.models import UserProfile, Role
# # from django.contrib.auth.models import User
#
# User = get_user_model()
#
#
# def read_csv_logs():
#     count = range(2742, 17542)
#     for n in count:
#         email = "account_test" + str(n) + "@gmail.com"
#         creator = UserProfile.objects.filter(pk=1).first()
#         username = "account_test" + str(n)
#         secret = "17aa6a04-bceb-431e-ab7e-df7a07f76a8d"
#         name = "account_test" + str(n)
#         remark = "remark"
#         role = Role.objects.filter(pk=2).first()
#         password = "123456a@"
#         user = User()
#         user.last_name = username
#         user.username = username
#         user.email = email
#         user.password = password
#         # user.sec
#         user.creator = creator
#         user.name = name
#         user.remark = remark
#         # user.role = role
#         user.save()
#         print("finished read csv")
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
#     read_csv_logs()
#
#
# if __name__ == '__main__':
#     print("Starting create user script...")
#     populate()
