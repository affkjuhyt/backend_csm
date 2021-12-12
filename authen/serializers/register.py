import logging
import re

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from rest_registration.api.serializers import DefaultRegisterUserSerializer
from rest_registration.exceptions import BadRequest
from apps.vadmin.utils.common import full_name

from apps.vadmin.permission.models import UserProfile

logger = logging.getLogger(__name__.split('.')[0])


class RegisterSerializer(DefaultRegisterUserSerializer):

    def validate_username(self, value):
        """
        1. Only contains alphanumeric characters, underscore and dot.
        2. Dot can't be at the end or start of a username (e.g .username / username.).
        3. Underscore and dot can't be next to each other (e.g user_.name).
        4. Underscore or dot can't be used multiple times in a row (e.g user__name / user..name).
        5. Number of characters must be between 2 to 32.
        """
        value = value.lower().strip()
        if not re.match('^(?=.{2,32}$)(?![.])(?!.*[_.]{2})[a-z0-9._]+(?<![.])$', value):
            logger.error(_(self.validate_username.__doc__))
            raise BadRequest(_('Please enter a valid username'))
        return value

    def validate(self, data):
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()
        if User.objects.filter(username=data["username"]).exists():
            raise BadRequest(_("Username already existed"))
        return data

    def create(self, validated_data):
        user = super().create(validated_data)
        UserProfile.objects.create(user_id=user.id, email=user.email, full_name=full_name(user.first_name, user.last_name))
        return user
