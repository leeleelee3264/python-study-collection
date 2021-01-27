from django.urls import path, include

urlpatterns = [
    path('admin', include('new_admin.urls'))
]