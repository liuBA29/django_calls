from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('clients/', client_list, name='client_list'),
    path('get_call_records/', get_call_records_view, name='get_call_records'),

    path('clients/<int:pk>/edit/', edit_client, name='edit_client'),
    path('clients/add/', add_client, name='add_client'),
    path('calls/', call_list, name='call_list'),

    path('api/data/', get_dynamic_data, name='get_dynamic_data'),
]
