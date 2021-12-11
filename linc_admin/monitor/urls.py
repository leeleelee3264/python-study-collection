from django.urls import path

from monitor import views

urlpatterns = [
    path('', views.index, name='monitor.index'),
    path('login/', views.do_login, name='monitor.login'),
    path('logout/', views.do_logout, name='monitor.logout'),

    path('device/list/', views.get_device_list, name='monitor.device_list'),
    path('device/info/', views.get_device_info, name='monitor.device_info'),

    path('device/<str:deveui>/trace/stop/', views.stop_trace, name='monitor.stop_trace'),
    path('device/<str:deveui>/trace/list/', views.get_trace_list, name='monitor.trace_list'),
]
