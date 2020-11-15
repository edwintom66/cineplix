from django.urls import path
from first_app import views

app_name = 'first_app'

urlpatterns = [
    path('',views.index,name='mainhome'),
    path('landing',views.landing),
    path('about',views.about,name='about'),
    # path('registration',views.registration),
]