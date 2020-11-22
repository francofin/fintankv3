from django.urls import path
from . import views

urlpatterns = [
    path('register_user', views.register_user, name="register_user"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('add_to_portfolio', views.add_to_portfolio, name='add_to_portfolio'),
    path('delete_stock/<stock_id>', views.delete_stock, name="delete_stock"),
]
