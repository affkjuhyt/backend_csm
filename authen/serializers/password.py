import datetime

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_registration.api.views.reset_password import ResetPasswordSigner
from rest_registration.exceptions import BadRequest
from rest_registration.utils.users import get_user_by_verification_id
from rest_registration.utils.verification import verify_signer_or_bad_request

from apps.vadmin.utils.times import convert_timestamp_to_datetime


class ResetPasswordSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    timestamp = serializers.IntegerField(required=True)
    signature = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate_password_confirm(self, password_confirm):
        password = self.initial_data.get('password')
        if password:
            if password_confirm != password:
                raise BadRequest(_("Passwords don't match"))
        return password_confirm

    def validate(self, attrs):
        data = attrs.copy()
        password = data.pop('password')
        data.pop('password_confirm')
        signer = ResetPasswordSigner(data)
        verify_signer_or_bad_request(signer)

        user = get_user_by_verification_id(data['user_id'])
        try:
            validate_password(password, user=user)
        except ValidationError as exc:
            raise BadRequest(exc.messages[0])
        created_time_signer = convert_timestamp_to_datetime(int(signer.get_signed_data()['timestamp']))
        last_update_password = user.userprofile.last_update_password
        if last_update_password and created_time_signer < last_update_password:
            raise BadRequest(_('Token expired.'))
        self.instance = user
        return {'password': password}

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.userprofile.last_update_password = datetime.datetime.utcnow()
        instance.userprofile.save()
        instance.save()
        return instance

    def create(self, validated_data):
        raise NotImplementedError(_('Not supported'))
