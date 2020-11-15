from django.urls import path
from . import views

urlpatterns = [
    path('screen', views.screen, name='screen'),
    path('screener', views.screener, name='screener'),
    path('stock_item/<str:item>/', views.stock_item, name='stock_item'),
]
