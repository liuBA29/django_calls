from django.conf import settings
from  django.conf.urls.static import  static

from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('check_incoming_calls/', check_incoming_calls, name='check_incoming_calls'),

    path('clients/', client_list, name='client_list'),
    path('get_call_records/', get_call_records_view, name='get_call_records'),

    path('clients/<int:pk>/edit/', edit_client, name='edit_client'),
    path('clients/<int:pk>/delete', delete_client, name='delete_client'),
    path('clients/add/', add_client, name='add_client'),
    path('calls/', call_list, name='call_list'),

    path('api/data/', get_dynamic_data, name='get_dynamic_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
