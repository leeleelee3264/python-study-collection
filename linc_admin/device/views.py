import datetime
import json
import random
import re
import string

import traceback

import requests
from django.db import transaction, DatabaseError, connection
from django.db.models import Count, Q
from django.db.models.aggregates import Max
from django.shortcuts import render
# Create your views here.
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from lxml import etree
from requests import Request

from common import util
from common.error_code import *
from device.models.ncs_device_info import NcsDeviceInfo
from device.models.ncs_deveui_range import NcsDeviceRange
from device.models.ncs_thingplug_info import NcsThingPlugInfo
from device.models.swatch_owner_event import SwatchAttendance
from device.models.swatch_device import SwatchDeviceInfo, SwatchDeviceExtendHistory, SwatchDeviceDelivery
from device.models.swatch_device_sn import SwatchDeviceSn
from device.models.swatch_device_user import SwatchDeviceUser, SwatchDeviceUserPush
from device.models.swatch_movement import SwatchMovement, SwatchMovementStat1d, SwatchMovementPattern
from device.models.swatch_trace import SwatchTraceHist, SwatchLocationReservation, SwatchTraceSummary
from device.models.swatch_user_info import SwatchUserInfo

_TABLE_CLASS = {
    0: '',
    1: 'table-success',
    2: 'table-warning',
    3: 'table-danger',
    -1: 'table-danger',
}

def is_dnx_deveui(deveui):
    return True

    if '70b3d5f5cafe0201' <= deveui <= '70b3d5f5cafe02d2':
        return True

    if '70b3d5f4cafe02d3' <= deveui <= '70b3d5f5cafe0399':
        return True

    return False


def make_product_key():
    _base = string.ascii_lowercase + string.digits

    return ''.join([random.choice(_base) for _ in range(16)])


def get_total_list(request):
    if request.method == 'GET':
        period = 0
        period_type = 'D'
        search_deveui = request.GET.get('device', '')

    elif request.method == 'POST':
        period = int(request.POST.get('txt_period', 0))
        period_type = request.POST.get('btn_type')
        print(period)
    else:
        return 405

    # rs = SwatchDeviceInfo.objects.filter(Q(deveui__startswith='70b3d5f5cafe') | Q(deveui__startswith='70b3d5f4cafe'))
    rs = SwatchDeviceInfo.objects.filter()
    if search_deveui != '':
        rs = rs.filter(deveui__contains=search_deveui)
    rs = rs.order_by('deveui')
    this_list = []
    for row in rs:
        row: SwatchDeviceInfo

        if not is_dnx_deveui(row.deveui):
            continue

        info = {
            'deveui': row.deveui,
            'last_uplink_time': '' if row.last_uplink_time is None else row.last_uplink_time.strftime('%Y.%m.%d %H:%M'),
            'last_gps_time': '' if row.last_location_time is None else row.last_location_time.strftime('%Y.%m.%d %H:%M'),
            'create_time': row.create_time.strftime('%Y.%m.%d %H:%M'),
            'level': row.get_recent_level(),
        }
        info['level_class'] = _TABLE_CLASS[info['level']]

        this_list.append(info)

    ctx = {
        'search_device': search_deveui,
        'now': dt_to_str(datetime.datetime.now()),
        'period': period,
        'this_list': this_list,
    }

    return render(request, 'device/total_list.html', context=ctx)


def get_open_list(request):
    if request.method == 'GET':
        period = 0
        period_type = 'D'
        search_deveui = request.GET.get('device', '')

    elif request.method == 'POST':
        period = int(request.POST.get('txt_period', 0))
        period_type = request.POST.get('btn_type')
        print(period)
    else:
        return 405

    now = timezone.now()
    rs = SwatchDeviceInfo.objects.filter(Q(deveui__startswith='70b3d5f5cafe') | Q(deveui__startswith='70b3d5f4cafe'))
    if search_deveui != '':
        rs = rs.filter(deveui__contains=search_deveui)
    rs = rs.filter(create_time__isnull=False)
    rs = rs.order_by('deveui')
    this_list = []
    for row in rs:
        row: SwatchDeviceInfo

        if not is_dnx_deveui(row.deveui):
            continue

        this_list.append({
            'deveui': row.deveui,
            'create_time': row.create_time.strftime('%Y.%m.%d %H:%M'),
            'expire_time': row.expire_date.strftime('%Y.%m.%d'),
            'old_uplink': row.last_uplink_time is None or (now - row.last_uplink_time).days > 7,
        })

    ctx = {
        'search_device': search_deveui,
        'now': dt_to_str(datetime.datetime.now()),
        'period': period,
        'this_list': this_list,
    }
    # pprint.pprint(ctx)

    return render(request, 'device/open_list.html', context=ctx)


def get_unopen_list(request):
    if request.method == 'GET':
        period = 0
        period_type = 'D'

    elif request.method == 'POST':
        period = int(request.POST.get('txt_period', 0))
        period_type = request.POST.get('btn_type')
        print(period)
    else:
        return 405

    rs = SwatchDeviceInfo.objects.filter(Q(deveui__startswith='70b3d5f5cafe') | Q(deveui__startswith='70b3d5f4cafe'))
    rs = rs.filter(create_time__isnull=True)
    rs = rs.order_by('deveui')
    this_list = []
    for row in rs:
        row: SwatchDeviceInfo

        if not is_dnx_deveui(row.deveui):
            continue

    ctx = {
        'now': dt_to_str(datetime.datetime.now()),
        'period': period,
        'this_list': this_list,
    }
    # pprint.pprint(ctx)

    return render(request, 'device/unopen_list.html', context=ctx)


def get_use_list(request):
    if request.method == 'GET':
        period = 0
        period_type = 'D'
        search_deveui = request.GET.get('device', '')

    elif request.method == 'POST':
        period = int(request.POST.get('txt_period', 0))
        period_type = request.POST.get('btn_type')
        print(period)
    else:
        return 405

    # now = datetime.datetime.now()
    now = timezone.now()
    ago = now - timezone.timedelta(days=7)
    print(now, ago)

    # ('70b3d5f5cafe0201', ''70b3d5f5cafe02d1'))
    # rs = SwatchDeviceInfo.objects.filter(deveui__startswith='70b3d5f5cafe02', power_yn='Y')
    rs = SwatchDeviceInfo.objects.filter(Q(deveui__startswith='70b3d5f5cafe') | Q(deveui__startswith='70b3d5f4cafe'))
    if search_deveui != '':
        rs = rs.filter(deveui__contains=search_deveui)
    rs = rs.filter(last_uplink_time__gt=ago)
    # if period > 0:
    #     if period_type == 'H':
    #         now += timezone.timedelta(hours=-period)
    #     else:
    #         now += timezone.timedelta(days=-period)
    #     print(now)
    #     rs = rs.filter(update_time__lte=now)
    rs = rs.order_by('deveui')

    this_list = []
    for row in rs:
        if not is_dnx_deveui(row.deveui):
            continue

        cnt_rs = SwatchTraceHist.objects.filter(device_id=row.deveui)
        cnt_rs = cnt_rs.values('trace_type').annotate(cnt=Count('trace_type'))
        dict_cnt = { _['trace_type']: _['cnt'] for _ in cnt_rs }

        this_list.append({
            'deveui': row.deveui,
            'last_uplink_time': '' if row.last_uplink_time is None else row.last_uplink_time.strftime('%m.%d %H:%M'),
            'last_gps_time': '' if row.last_location_time is None else row.last_location_time.strftime('%m.%d %H:%M'),
            'emergency_count': dict_cnt.get('E', 0),
            'track_count': dict_cnt.get('R', 0),
            'safezone_count': dict_cnt.get('S', 0),
        })

    ctx = {
        'search_device': search_deveui,
        'now': dt_to_str(datetime.datetime.now()),
        'period': period,
        'this_list': this_list,
    }

    return render(request, 'device/use_list.html', context=ctx)


def get_owner_list(request):
    search_deveui = request.GET.get('device', '')
    period = 0

    rs = SwatchDeviceInfo.objects.filter(owner_id__gt=0)
    if search_deveui != '':
        rs = rs.filter(deveui__contains=search_deveui)
    rs = rs.order_by('deveui')

    this_list = []
    owner_info = {}
    for row in rs:
        owner = owner_info.get(row.owner_id, None)
        if owner is None:
            owner = SwatchUserInfo.objects.get(id=row.owner_id)
            owner_info[row.owner_id] = owner

        this_list.append({
            'deveui': row.deveui,
            'owner_id': row.owner_id,
            'owner_name': owner.name,
            'phone_no': owner.get_normalized_phone_no(),
            'app_os': ('iOS', 'Android')[owner.app_os_type == 'A'],
            'has_gcm': owner.has_gcm_token(),
            'last_login_time': owner.last_login.strftime('%Y.%m.%d %H:%M:%S'),
        })

    ctx = {
        'search_device': search_deveui,
        'now': dt_to_str(datetime.datetime.now()),
        'period': period,
        'this_list': this_list,
    }

    return render(request, 'device/owner_list.html', context=ctx)


def get_expire_list(request):
    search_deveui = request.GET.get('device', '').strip()[:16]

    period = 0
    now = timezone.now()

    rs = SwatchDeviceInfo.objects.all()
    if search_deveui != '':
        rs = rs.filter(deveui__contains=search_deveui)
    rs = rs.order_by('deveui')

    this_list = []
    for row in rs:
        grade = 1
        if now.date() > row.expire_date:
            grade = -1
        elif (now + timezone.timedelta(days=30)).date() > row.expire_date:
            grade = 0

        this_list.append({
            'deveui': row.deveui,
            'fw_ver': row.fw_ver,
            'fw_mode': row.fw_mode,
            'lora_period': row.lora_period_min,
            'expire_time': row.expire_date.strftime('%Y.%m.%d'),
            'grade': grade,
        })

    ctx = {
        'search_device': search_deveui,
        'now': dt_to_str(datetime.datetime.now()),
        'period': period,
        'this_list': this_list,
    }

    return render(request, 'device/expire_list.html', context=ctx)


def get_statistics(request):
    sql = 'SELECT a.id, a.deveui, a.combo, a.attend_date from swatch.t_swatch_attendance a '\
        'INNER JOIN (SELECT deveui, max(id) as id from swatch.t_swatch_attendance group by deveui) b on a.id = b.id '\
        'order by a.combo desc'
    rs = SwatchAttendance.objects.raw(sql)

    max_combo_rs = SwatchAttendance.objects.values('device_id').annotate(max_combo=Max('combo'))
    max_combo_info = { row['device_id']: row['max_combo'] for row in max_combo_rs }

    now = datetime.datetime.now()
    this_list = []
    for row in rs:
        yesterday = (now + timezone.timedelta(days=-1)).date()

        grade = 1
        if row.attend_date < yesterday:
            grade = -1
        elif row.attend_date == yesterday:
            grade = 0

        this_list.append({
            'grade': grade,
            'deveui': row.device_id,
            'combo': row.combo,
            'max_combo': max_combo_info[row.device_id],
            'attend_date': row.attend_date.strftime('%Y-%m-%d'),
        })

    ctx = {
        'this_list': this_list,
    }

    return render(request, 'device/statistics.html', context=ctx)


def dt_to_str(dt: datetime.datetime):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def get_gap(_sec):
    sec = _sec

    dd, sec = divmod(sec, 24 * 3600)
    hh, sec = divmod(sec, 3600)
    mm, sec = divmod(sec, 60)
    ss = sec

    return int(dd), int(hh), int(mm), int(ss)


@require_http_methods(['POST'])
def set_begin(request):
    param = json.loads(request.body)

    days = param.get('days')
    target = set(param.get('target', []))

    if days is None or type(days) is not int:
        return util.res_json(EXTEND_EXPIRE_NO_DAYS)

    if len(target) == 0:
        return util.res_json(EXTEND_EXPIRE_NO_TARGET)

    if SwatchDeviceInfo.objects.filter(deveui__in=target).count() != len(target):
        return util.res_json(EXTEND_EXPIRE_INVALID_TARGET)

    with transaction.atomic():
        for device_id in target:
            device = SwatchDeviceInfo.objects.get(deveui=device_id)

            now = datetime.datetime.now()
            now += datetime.timedelta(days=days)

            device.begin_date = now

            device.save(update_fields=['begin_date'])

    return util.res_json()


@require_http_methods(["POST"])
def extend_expire(request):
    param = json.loads(request.body)

    days = param.get('days')
    target = set(param.get('target', []))
    is_extend = param.get('is_extend', True)

    if days is None or type(days) is not int:
        return util.res_json(EXTEND_EXPIRE_NO_DAYS)

    if len(target) == 0:
        return util.res_json(EXTEND_EXPIRE_NO_TARGET)

    if SwatchDeviceInfo.objects.filter(deveui__in=target).count() != len(target):
        return util.res_json(EXTEND_EXPIRE_INVALID_TARGET)

    with transaction.atomic():
        for device_id in target:
            device = SwatchDeviceInfo.objects.get(deveui=device_id)
            prev_expire_date = device.expire_date

            if is_extend is True:
                device.expire_date += datetime.timedelta(days=days)
            else:
                now = datetime.datetime.now()
                now += datetime.timedelta(days=days)

                device.expire_date = now

            device.save(update_fields=['expire_date'])

            #
            o = SwatchDeviceExtendHistory()

            o.deveui = device_id
            o.is_extend = is_extend
            o.days = days
            o.prev_expire_date = prev_expire_date
            o.expire_date = device.expire_date

            o.save()

    return util.res_json()

@require_http_methods(["POST"])
def change_fw_mode(request):
    param = json.loads(request.body)

    fw_mode = param.get('fw_mode')
    target = set(param.get('target', []))

    if fw_mode is None or type(fw_mode) is not int or fw_mode not in (0, 1, 2, 3, 4, 5, 8):
        return util.res_json(CHANGE_FW_MODE_NO_MODE)

    if len(target) == 0:
        return util.res_json(CHANGE_NO_TARGET)

    if SwatchDeviceInfo.objects.filter(deveui__in=target).count() != len(target):
        return util.res_json(CHANGE_INVALID_TARGET)

    with transaction.atomic():
        for device_id in target:
            device = SwatchDeviceInfo.objects.get(deveui=device_id)

            device.fw_mode = fw_mode

            device.save(update_fields=['fw_mode'])

    return util.res_json()


@require_http_methods(["POST"])
def change_lora_period(request):
    param = json.loads(request.body)

    lora_period = param.get('lora_period')
    target = set(param.get('target', []))

    if lora_period is None or type(lora_period) is not int or lora_period <= 0:
        return util.res_json(CHANGE_LORA_PERIOD_NO_PERIOD)

    if len(target) == 0:
        return util.res_json(CHANGE_NO_TARGET)

    if SwatchDeviceInfo.objects.filter(deveui__in=target).count() != len(target):
        return util.res_json(CHANGE_INVALID_TARGET)

    with transaction.atomic():
        for device_id in target:
            device = SwatchDeviceInfo.objects.get(deveui=device_id)

            device.lora_period_min = lora_period

            device.save(update_fields=['lora_period_min'])

    return util.res_json()


@require_http_methods(["POST"])
def deliver_start(request):
    param = json.loads(request.body)
    expire_days = param.get('expire_days')
    start_date = param.get('start_date', '').replace('-', '')
    target = set(param.get('target', []))

    if len(target) == 0:
        return util.res_json(DELIVER_NO_TARGET)

    if expire_days <= 0:
        return util.res_json(DELIVER_WRONG_EXPIRE_DAYS)

    today = datetime.datetime.today().date()
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y%m%d').date()
        if start_date <= today:
            return util.res_json(DELIVER_MORE_START_DATE)
    except ValueError:
        return util.res_json(DELIVER_WRONG_START_DATE)

    rs = SwatchDeviceDelivery.objects.exclude(status=SwatchDeviceDelivery.STATUS_HOME).filter(device_id__in=target)
    use_device_list = rs.values_list('device_id', flat=True).order_by('device_id')
    print('DELIVERY DEVICE LIST: ', use_device_list)
    if len(use_device_list) > 0:
        return util.res_json(DELIVER_ALREADY_USE)

    rs = SwatchDeviceInfo.objects.filter(deveui__in=target, expire_date__gte=today)
    valid_device_list = rs.values_list('deveui', flat=True).order_by('deveui')
    print('VALID DEVICE LIST: ', valid_device_list)
    if len(valid_device_list) > 0:
        return util.res_json(DELIVER_NOT_EXPIRE)

    with transaction.atomic():
        for deveui in target:
            o = SwatchDeviceInfo.objects.get(deveui=deveui)

            o.trace_id = 0
            o.trace_req_user_id = 0

            o.owner_id = 0
            o.owner_latitude = 0
            o.owner_longitude = 0
            o.owner_height = 0
            o.owner_location_time = None

            o.save()

            SwatchAttendance.objects.filter(device_id=deveui).delete()
            SwatchDeviceUser.objects.filter(device_id=deveui, user__is_admin=False).delete()
            SwatchDeviceUserPush.objects.filter(device_id=deveui, user__is_admin=False).delete()
            SwatchLocationReservation.objects.filter(device_id=deveui, user__is_admin=False).delete()
            SwatchMovement.objects.filter(device_id=deveui).delete()
            SwatchMovementStat1d.objects.filter(device_id=deveui).delete()
            SwatchMovementPattern.objects.filter(device_id=deveui).delete()
            SwatchTraceHist.objects.filter(device_id=deveui).delete()

            # 배달 기록 입력
            o = SwatchDeviceDelivery()

            o.device_id = deveui
            o.status = SwatchDeviceDelivery.STATUS_DELIVER
            o.days = expire_days
            o.start_date = start_date

            o.save(force_insert=True)

    return util.res_json()


def remove_history(request):
    param = json.loads(request.body)
    target = set(param.get('target', []))

    if len(target) == 0:
        return util.res_json(DELIVER_NO_TARGET)

    with transaction.atomic():
        for deveui in target:
            o = SwatchDeviceInfo.objects.get(deveui=deveui)

            o.trace_id = 0
            o.trace_req_user_id = 0
            o.battery_level = 0

            o.begin_date = datetime.datetime.now()

            o.latitude = None
            o.longitude = None
            o.height = 0.0

            o.gw_latitude = None
            o.gw_longitude = None
            o.last_location_time = None
            o.last_uplink_time = None

            o.owner_id = 0
            o.owner_latitude = 0
            o.owner_longitude = 0
            o.owner_height = 0
            o.owner_location_time = None

            o.save()

            SwatchAttendance.objects.filter(device_id=deveui).delete()
            SwatchDeviceUser.objects.filter(device_id=deveui, user__is_admin=False).delete()
            SwatchDeviceUserPush.objects.filter(device_id=deveui, user__is_admin=False).delete()
            SwatchLocationReservation.objects.filter(device_id=deveui, user__is_admin=False).delete()
            SwatchMovement.objects.filter(device_id=deveui).delete()
            SwatchMovementStat1d.objects.filter(device_id=deveui).delete()
            SwatchMovementPattern.objects.filter(device_id=deveui).delete()
            SwatchTraceHist.objects.filter(device_id=deveui).delete()
            SwatchTraceSummary.objects.filter(device_id=deveui).delete()

    return util.res_json()


@require_http_methods(['GET', 'POST'])
def new_device(request):
    rs = NcsThingPlugInfo.objects.all().values_list('tp_id', flat=True).using('ncs')
    rs = rs.order_by('tp_id')
    tp_id_list = list(rs)

    def make_app_key():
        return ''.join([f'{random.randint(1, 255):02x}' for _ in range(16)])

    if request.method == 'GET':
        search_deveui = request.GET.get('device', '')
        country_code = request.GET.get('country_code', '')

        rs = SwatchDeviceSn.objects.filter(deveui__startswith='5357')
        if search_deveui != '':
            rs = rs.filter(deveui__contains=search_deveui)
        rs = rs.order_by('deveui')

        device_list = []
        for row in rs:
            row.country_code = bytes.fromhex(row.deveui[4:8]).decode()
            if country_code != '' and country_code != row.country_code:
                continue
            row.appkey = row.appkey or ''

            device_list.append({
                'country_code': row.country_code,
                'deveui': row.deveui,
                'product_key': row.serial_no,
                'product_key2': '-'.join(re.findall('.{4}', row.serial_no)),
                'app_key': row.appkey,
                'app_key2': '-'.join(re.findall('.{2}', row.appkey))
            })

        ctx = {
            'search_device': search_deveui,
            'this_list': device_list,
            'tp_list': tp_id_list,
            'country_code': country_code,
        }

        return render(request, 'device/new.html', context=ctx)

    # POST request
    param = json.loads(request.body)
    tp_id = param.get('tp_id', '').strip()
    country_code = param.get('country_code', '').upper()

    if tp_id not in tp_id_list:
        return util.res_json(NEW_DEVICE_INVALID_TP_ID)

    if len(country_code) != 2:
        return util.res_json(NEW_DEVICE_WRONG_COUNTRY_CODE)

    # make S W K R 1809####
    now = datetime.datetime.now()
    this_prefix = f'SW{country_code}'.encode().hex()

    rs = SwatchDeviceSn.objects.filter(deveui__startswith=this_prefix).order_by('-deveui')[:1]
    if len(rs) == 0:
        seq = 1
    else:
        seq = int(rs[0].deveui[-4:], 16) + 1 % 0xFFFF

    app_key = make_app_key()
    product_key = make_product_key()
    deveui = f'{this_prefix}{now.strftime("%y%m")}{seq:04x}'

    try:
        with transaction.atomic():
            # t_swatch_device_sn
            o = SwatchDeviceSn()

            o.deveui = deveui
            o.serial_no = product_key
            o.appkey = app_key

            o.save()

            # t_swatch_device_info
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO swatch.t_swatch_device_info (deveui, appeui) VALUES ('%s', '%s') " % (deveui, '0'))

            # t_ncs_device_info
            o = NcsDeviceInfo()

            o.deveui = deveui
            o.appeui = '0'
            o.if_type = (tp_id[0:1], 'T')[tp_id in ('DNX', 'NABLE')]
            o.tp_id = tp_id

            o.save(using='ncs')
    except:
        traceback.print_exc()
        return util.res_json(NEW_DEVICE_FAIL)

    rs = NcsDeviceRange.objects.all().using('ncs')
    for row in rs:
        if row.deveui_from <= deveui <= row.deveui_to:
            valid_range = True
            break
    else:
        valid_range = False

    data = {
        'deveui': deveui,
        'product_key': product_key,
        'app_key': app_key,
        'valid_range': valid_range,
    }

    return util.res_json(data=data)


@require_http_methods(['GET', 'POST'])
def new_virtual_device(request):
    if request.method == 'GET':
        search_deveui = request.GET.get('device', '')

        rs = SwatchDeviceSn.objects.filter(deveui__startswith='vv')
        if search_deveui != '':
            rs = rs.filter(deveui__contains=search_deveui)
        rs = rs.order_by('deveui')

        device_list = []
        for row in rs:
            device_list.append({
                'deveui': row.deveui,
                'product_key': row.serial_no,
                'product_key2': '-'.join(re.findall('.{4}', row.serial_no)),
            })

        ctx = {
            'search_device': search_deveui,
            'this_list': device_list,
        }

        return render(request, 'device/virtual.html', context=ctx)

    # POST request
    today = datetime.datetime.now()
    yyyymm = today.strftime('%Y%m')
    this_prefix = f'vv{yyyymm}cafe'

    rs = SwatchDeviceInfo.objects.filter(deveui__startswith=this_prefix).order_by('-deveui')[0:1]
    if len(rs) == 0:
        seq = 1
    else:
        seq = int(rs[0].deveui[-4:], 16) + 1 % 0xFFFF

    product_key = make_product_key()
    deveui = f'{this_prefix}{seq:04x}'
    try:
        with transaction.atomic():
            # t_swatch_device_sn
            o = SwatchDeviceSn()

            o.deveui = deveui
            o.serial_no = product_key

            o.save(force_insert=True)

            # t_swatch_device_info
            # with connection.cursor() as cursor:
            #     cursor.execute("INSERT INTO swatch.t_swatch_device_info (deveui, appeui) VALUES ('%s', '%s') " % (deveui, '0'))

            o = SwatchDeviceInfo()

            o.deveui = deveui

            o.appeui = '0'
            o.trace_type = SwatchDeviceInfo.TRACE_TYPE_NONE
            o.power_yn = 'N'

            o.fw_mode = 0
            o.lora_period_min = 0
            o.expire_date = today

            o.save(force_insert=True)
    except:
        traceback.print_exc()
        return util.res_json(NEW_DEVICE_FAIL)

    return util.res_json()


@require_http_methods(['GET', 'POST'])
def atility_token(request):
    if request.method == 'GET':
        rs = NcsThingPlugInfo.objects.filter(Q(tp_id__startswith='Atility')|Q(tp_id='TELCO')).order_by('tp_id').using('ncs')
        this_list = []
        for row in rs:
            this_list.append({
                'tp_id': row.tp_id,
                'token': row.tp_ukey.split(' ')[-1],
            })

        ctx = {
            'this_list': this_list,
        }

        return render(request, 'device/atility_token.html', context=ctx)

    # POST request
    param = json.loads(request.body)

    tp_id = param.get('tp_id', '').strip()
    token = param.get('token', '').strip()
    print(tp_id, token)

    if tp_id == '' or token == '':
        return util.res_json(PARAM_ERROR)

    kwargs = {
        'tp_ukey': f'Bearer {token}'
    }
    NcsThingPlugInfo.objects.filter(tp_id=tp_id).using('ncs').update(**kwargs)

    return util.res_json()


@require_http_methods(['GET'])
def manage_callback(request):
    search_deveui = request.GET.get('device', '')

    rs = NcsDeviceInfo.objects.filter(if_type='T')
    if search_deveui != '':
        rs = rs.filter(deveui__contains=search_deveui)
    rs = rs.order_by('deveui').using('ncs')

    this_list = []
    for row in rs:
        this_list.append({
            'deveui': row.deveui,
            'appeui': row.appeui,
            'tp_id': row.tp_id,
            'if_type': row.if_type,
            'subscribe_uplink': row.tp_subs_ul_yn == 'Y',
        })

    ctx = {
        'search_device': search_deveui,
        'this_list': this_list,
    }

    return render(request, 'device/manage/callback_list.html', context=ctx)


@require_http_methods(['POST'])
def manage_callback_add(request):
    # POST request
    param = json.loads(request.body)
    deveui = param.get('deveui', '')

    print(deveui)
    rs = NcsDeviceInfo.objects.filter(deveui=deveui).using('ncs')
    if len(rs) == 0:
        return util.res_json(-1)
    ncs_device_info = rs[0]

    ncs_tp_info = NcsThingPlugInfo.objects.filter(tp_id=ncs_device_info.tp_id).using('ncs')[0]
    lt_id = ncs_device_info.appeui[-8:] + deveui

    try:
        ns_m2m = 'http://www.onem2m.org/xml/protocols'
        namespaces = {
            'm2m': ns_m2m,
            'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        }

        doc = etree.Element('{%s}sub' % ns_m2m, nsmap=namespaces)

        elm_enc = etree.SubElement(doc, 'enc')
        elm_rss = etree.SubElement(elm_enc, 'rss')
        elm_rss.text = '1'

        cb_url = f'https://tpi.dnx.kr:443/cb/thingplug/uplink/{deveui}'
        elm_nu = etree.SubElement(doc, 'nu')
        elm_nu.text = f'HTTP|{cb_url}'

        elm_pn = etree.SubElement(doc, 'pn')
        elm_pn.text = '1'

        elm_nct = etree.SubElement(doc, 'nct')
        elm_nct.text = '2'

        # print(etree.tostring(doc, pretty_print=True).decode())

    except Exception as e:
        print(e)

    xml_body = etree.tostring(doc)

    conn = requests.session()
    my_header = {
        'Accept': 'application/xml',
        'X-M2M-RI': lt_id,
        'X-M2M-Origin': 'Origin',
        'X-M2M-NM': 'uplink',
        'Content-Type': 'application/vnd.onem2m-res+xml;ty=23',
        # 'Content-Length': f'{len(xml_body)}',
        'locale': 'en',
        'uKey': ncs_tp_info.tp_ukey,
    }
    conn.headers.update(my_header)

    url = f'http://{ncs_tp_info.tp_domain}:{ncs_tp_info.tp_port}/{ncs_device_info.appeui}/v1_0/remoteCSE-{lt_id}/container-LoRa'
    res = conn.post(url, data=etree.tostring(doc, encoding='UTF-8', xml_declaration=True, standalone=True).decode())
    # res = conn.send(prepare_request, stream=etree.tostring(doc))
    # print(res.request.url)
    # print(res.request.headers)
    # print(res.request.body)
    print(res.status_code, res.text)

    if res.status_code == 201:
        try:
            ncs_device_info.tp_subs_ul_yn = 'Y'
            ncs_device_info.save(force_update=True, update_fields=('tp_subs_ul_yn', ))
        except:
            return util.res_json(DB_ERROR)
    else:
        print(res.status_code, res.text)

    return util.res_json()


@require_http_methods(['POST'])
def manage_callback_remove(request):
    # POST request
    param = json.loads(request.body)
    deveui = param.get('deveui', '')

    print(deveui)
    rs = NcsDeviceInfo.objects.filter(deveui=deveui).using('ncs')
    if len(rs) == 0:
        return util.res_json(-1)
    ncs_device_info = rs[0]

    ncs_tp_info = NcsThingPlugInfo.objects.filter(tp_id=ncs_device_info.tp_id).using('ncs')[0]
    lt_id = ncs_device_info.appeui[-8:] + deveui

    conn = requests.session()
    conn.headers.update({
        'X-M2M-RI': lt_id,
        'X-M2M-Origin': 'Origin',
        'uKey': ncs_tp_info.tp_ukey,
    })

    url = f'http://{ncs_tp_info.tp_domain}:{ncs_tp_info.tp_port}/{ncs_device_info.appeui}/v1_0/remoteCSE-{lt_id}/container-LoRa/subscription-uplink'
    res = conn.delete(url=url)
    print(res.text)

    if res.status_code != requests.codes.ok:
        print(url, res.status_code)
        return util.res_json(-1)

    ncs_device_info.tp_subs_ul_yn = 'N'

    try:
        ncs_device_info.save(update_fields=['tp_subs_ul_yn'])
    except:
        return util.res_json(DB_ERROR)

    return util.res_json()
