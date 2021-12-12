import logging

from django.contrib.auth import get_user_model
from django.db import models
from apps.vadmin.utils.base_models import BaseTimeStampModel

UserModel = get_user_model()
logger = logging.getLogger(__name__.split('.')[0])


class UserFollowing(BaseTimeStampModel):

    user_id = models.ForeignKey(UserModel, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(UserModel, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]

        ordering = ["-date_added"]

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"

