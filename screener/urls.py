from django.urls import path
from . import views

urlpatterns = [
    path('screener', views.screener, name='screener'),
]
