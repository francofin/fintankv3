from django.urls import path
from . import views

urlpatterns = [
    path('stock_search', views.stock_search, name='stock_search'),
]
