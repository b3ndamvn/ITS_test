from django.urls import path

from . import views

urlpatterns = [
    path('moneyusers/', views.ListMoneyUserAPIView.as_view(), name='get_users'),
    path('send_money/', views.MoneyPipeAPIView.as_view(), name='send_money'),
]
