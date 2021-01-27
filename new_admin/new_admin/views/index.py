import logging

from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from common.error_code import *
from common.reponse_formatter import res_json
from new_admin.models.admin_user import AdminUser

logger = logging.getLogger(__name__)


@require_http_methods(['GET', 'POST'])
def index(request):

    if request.method == 'GET':
        return render(request, 'new_admin/index.html')
    elif request.method == 'POST':
        data = {
            'info': 'you got response from post method'
        }
        return res_json(OK, data)
    else:
        return res_json(ERROR_NOT_SUPPORTED_METHOD)


@require_http_methods(['GET'])
def db_test(request):

    db_result = AdminUser.objects.get(id=1)

    return res_json(OK, db_result.login_id)