import os

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from qliq import views

urlpatterns = [
    path('register/', views.register, name='qliq.register'),
    path('ya/', views.ya, name='qliq.ya'),
    path('sos/', views.sos, {'is_sos': True}, name='qliq.sos'),
    path('sos/voice/', views.sos_voice, name='qliq.sos_voice'),
    path('sos/voice/upload/', views.sos_voice_upload, name='qliq.sos_voice_upload'),
    path('here/', views.sos, {'is_sos': False}, name='qliq.here'),
]

urlpatterns += static('upload/', document_root=os.path.join(settings.MEDIA_ROOT, 'qliq'))
urlpatterns += static('firmware/', document_root=os.path.join(settings.BASE_DIR, '../qliq/firmware'))
