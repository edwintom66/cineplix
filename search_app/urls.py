from django.urls import path
from . import views

app_name = 'search_app'

urlpatterns = [
    path('',views.search_api_func,name='search_api')
]