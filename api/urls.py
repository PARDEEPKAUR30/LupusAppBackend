from django.urls import path
from . import views 

urlpatterns = [
    path('predict/', views.predict_lupus, name='predict_lupus'),
]
