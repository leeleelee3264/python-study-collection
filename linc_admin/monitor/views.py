import datetime
import json
import random

import requests
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from common import util
# Create your views here.
from common.error_code import *
from device.models.swatch_device import SwatchDeviceInfo
from device.models.swatch_device_user import SwatchDeviceUser
from device.models.swatch_trace import SwatchTraceDetail

# _marker = "http://maps.google.com/mapfiles/ms/micons/%s.png"
_marker = f"{settings.STATIC_URL}images/icon/%s.png"


def index(request):
    if not is_login(request):
        return redirect('monitor.login')

    return redirect('monitor.device_list')


@require_http_methods(['GET', 'POST'])
def do_login(request):
    if is_login(request):
        return redirect('monitor.index')

    if request.method == 'GET':
        return render(request, 'monitor/login.html')
    else:
        params = json.loads(request.body)

        phone_no = params.get('login_id', '')
        password = params.get('login_password', '')

        user = authenticate(request, phone_no=phone_no, password=password)
        if user is not None:
            login(request, user)
        else:
            return util.res_json(error_code=LOGIN_FAIL)

        return util.res_json()


def do_logout(request):
    logout(request)

    return redirect('monitor.index')


@require_http_methods(['GET', 'POST'])
def get_device_list(request):
    if not is_login(request):
        if request.method == 'GET':
            return redirect('monitor.login')
        else:
            return util.res_json(LOGIN_REQUIRED)

    def make_context():
        rs = SwatchDeviceUser.objects.filter(user_id=request.user.id).select_related('device')
        rs = rs.order_by('nickname')

        this_list = []
        emergency_list = []
        center_lat = 0.0
        center_lng = 0.0
        last_location_time = None
        for row in rs:
            lat = row.device.get_latitude()
            lng = row.device.get_longitude()

            if lat != 0.0 and lng != 0.0:
                if last_location_time is None or last_location_time < row.device.last_location_time:
                    last_location_time = row.device.last_location_time
                    center_lat = lat
                    center_lng = lng

            if row.device.battery_level is None:
                row.device.battery_level = 0

            # if row.device_id == '70b3d5f5cafe02c4':
            #     row.device.trace_type = 'E'

            info = {
                'device_id': row.device_id,
                'nickname': row.nickname,
                'photo_url': row.photo_url,
                'trace_type': row.device.trace_type,
                'latitude': lat,
                'longitude': lng,
                # 'last_location_time': row.device.get_last_location_time(),
                'is_valid': row.device.is_valid(),
                'is_sleep': row.device.is_sleep(),
                'is_poweroff': row.device.is_poweroff(),
            }

            if not info['is_valid']:
                info['marker'] = _marker % 'orange'
            elif info['is_sleep'] or info['is_poweroff']:
                info['marker'] = _marker % 'gray'
            else:
                if info['trace_type'] == 'E':
                    info['marker'] = '/static/images/icon/siren.gif'
                elif info['trace_type'] == 'S':
                    info['marker'] = _marker % 'purple'
                elif info['trace_type'] == 'R':
                    info['marker'] = _marker % 'blue'
                else:
                    info['marker'] = _marker % 'green'

            this_list.append(info)
            if info['trace_type'] == 'E':
                emergency_list.append(info)

        _ctx = {
            'center_latitude': center_lat,
            'center_longitude': center_lng,
            'this_list': this_list,
            'emergency_list': emergency_list,
        }

        return _ctx

    if request.method == 'GET':
        ctx = make_context()
        ctx['range'] = range(1, 31)

        return render(request, 'monitor/device/list.html', context=ctx)
    else:
        return util.res_json(data=make_context())


@require_http_methods('POST')
@login_required
def get_device_info(request):
    params = json.loads(request.body)
    deveui = params.get('device_id', '')

    try:
        o = SwatchDeviceInfo.objects.get(deveui=deveui)
    except ObjectDoesNotExist:
        return util.res_json(-1)

    rs = SwatchDeviceUser.objects.select_related('user').filter(device_id=deveui)
    guardian_list = []
    for row in rs:
        if request.user.id != row.user.id and row.user.is_admin is True:
            continue

        guardian_list.append({
            'phone_no': row.user.phone_no,
            'name': row.user.name,
        })

    data = {
        'now': int(datetime.datetime.now().timestamp()),
        # 'photo_url': SwatchDeviceUser.objects.filter(device_id=deveui, user_id=request.user.id)[0].photo_url,
        'battery_level': o.battery_level,
        'expire_date': o.expire_date,
        'last_location_time': o.get_last_location_time(),
        'gw_latitude': o.get_gw_latitude(),
        'gw_longitude': o.get_gw_longitude(),
        'gw_location_time': o.get_last_uplink_time(),
        'guardian_list': guardian_list,
    }

    return util.res_json(data=data)

@require_http_methods('POST')
@login_required
def stop_trace(request, deveui):
    try:
        device = SwatchDeviceInfo.objects.get(deveui=deveui)
    except ObjectDoesNotExist:
        return util.res_json(PARAM_ERROR)

    if device.trace_type == 'N':
        return util.res_json(data={
            'not_available': True,
        })

    url = f'{settings.SW_REST_URL}/safewatch/device/{deveui}/trace/stop'
    res = requests.post(url, json={'session_key': request.user.session_key})
    print(res.status_code, res.text)

    return util.res_json(0)


@require_http_methods('POST')
@login_required
def get_trace_list(request, deveui):
    try:
        device = SwatchDeviceInfo.objects.get(deveui=deveui)
    except ObjectDoesNotExist:
        return util.res_json(PARAM_ERROR)

    if device.trace_type == 'N':
        return util.res_json(-1)

    rs = SwatchTraceDetail.objects.filter(trace_id=device.trace_id)
    rs = rs.order_by('trace_detail_id')

    trace_list = []
    for row in rs:
        latitude = row.get_latitude()
        longitude = row.get_longitude()

        if latitude == 0.0 and longitude == 0.0:
            continue

        # latitude += random.random() - 0.5
        # longitude += random.random() - 0.5

        trace_list.append({
            'latitude': latitude,
            'longitude': longitude,
            'create_time': row.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'create_timestamp': int(row.create_time.timestamp()),
        })

    data = {
        'trace_list': trace_list,
    }

    return util.res_json(data=data)

def is_login(request):
    return request.session.get('auth_monitor', False)
