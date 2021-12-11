from django.core.exceptions import ObjectDoesNotExist

from device.models.swatch_user_info import SwatchUserInfo


class SWBackend:
    def authenticate(self, request, phone_no=None, password=None):
        try:
            this_user = SwatchUserInfo.objects.get(phone_no=phone_no)
        except ObjectDoesNotExist:
            return None

        if this_user.get_password() != password:
            return None

        request.session['auth_monitor'] = True

        return this_user

    def get_user(self, user_id):
        try:
            return SwatchUserInfo.objects.get(pk=user_id)
        except SwatchUserInfo.DoesNotExist:
            return None
