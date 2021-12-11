from django.urls import path

from device import views

urlpatterns = [
    path('total_list/', views.get_total_list, name='device.total_list'),
    path('use_list/', views.get_use_list, name='device.use_list'),
    path('open_list/', views.get_open_list, name='device.open_list'),
    path('unopen_list/', views.get_unopen_list, name='device.unopen_list'),
    path('owner_list/', views.get_owner_list, name='device.owner_list'),
    path('expire_list/', views.get_expire_list, name='device.expire_list'),
    path('statistics/', views.get_statistics, name='device.statistics'),

    path('set_begin/', views.set_begin, name='device.set_begin'),
    path('extend_expire/', views.extend_expire, name='device.extend_expire'),
    path('change/fw_mode/', views.change_fw_mode, name='device.change_fw_mode'),
    path('change/lora_period/', views.change_lora_period, name='device.change_lora_period'),
    path('deliver/start/', views.deliver_start, name='device.deliver_start'),
    path('remove_history/', views.remove_history, name='device.remove_history'),

    path('new/', views.new_device, name='device.new'),
    path('virtual/new/', views.new_virtual_device, name='device.virtual_new'),
    path('atility_token/', views.atility_token, name='device.atility_token'),
    path('manage/callback/', views.manage_callback, name='device.manage_callback'),
    path('manage/callback/add', views.manage_callback_add, name='device.manage_callback_add'),
    path('manage/callback/remove', views.manage_callback_remove, name='device.manage_callback_remove'),
]
