from django.urls import path

from rang import views

urlpatterns = [
    path('register/', views.register, name='rang.register'),
    path('sos/', views.sos, {'is_sos': True}, name='rang.sos'),
    path('here/', views.sos, {'is_sos': False}, name='rang.here'),
]
