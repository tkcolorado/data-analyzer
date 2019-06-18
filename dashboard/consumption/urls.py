from django.urls import path
from . import views

urlpatterns = [
    path('', views.front_page, name='home'),
    path('summary', views.summary, name='summary' ),
    path('details', views.details, name='details'),
]