from django.urls import path
from . import views 

urlpatterns = [
    path('predict/', views.predict_lupus, name='predict_lupus'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('downloads/', views.downloads, name='downloads'),
    path('download-apk/', views.download_apk, name='download-apk'),
    path('lupuscheck_app/', views.lupuscheck_app, name='lupuscheck_app')
]
