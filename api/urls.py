from django.urls import path
from . import views 

urlpatterns = [
    path('predict/', views.predict_lupus, name='predict_lupus'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy')
]
