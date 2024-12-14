# urls.py

from django.conf import settings
from  django.conf.urls.static import  static

from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('clients/', client_list, name='client_list'),
    path('clients/<int:pk>/edit/', edit_client, name='edit_client'),
    path('clients/<int:pk>/delete', delete_client, name='delete_client'),
    path('clients/add/', add_client, name='add_client'),
    path('client/<int:pk>/', client_detail, name='client_detail'),

    path('calls/', call_list, name='call_list'),

    path('get-call-status/', get_call_status, name='get_call_status'),

    path('random-number/', random_number_page, name='random_number'),
    path('active-calls/', active_calls_page, name='active-calls'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
