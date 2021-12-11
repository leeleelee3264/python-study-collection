from django.urls import path

from push import views

urlpatterns = [
    path('owner/', views.send_owner, name='push.send_owner'),
]
