from django.db import models


class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=16)
    content_id = models.CharField(max_length=16)
    event = models.CharField(max_length=200)
    type = models.CharField(max_length=30, null=True)
    session_id = models.CharField(max_length=128)

    def __str__(self):
        return "user_id: {}, content_id: {}, event: {}".format(self.user_id, str(self.content_id), self.event)
