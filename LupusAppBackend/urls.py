from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to LupusApp Backend")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Assuming your app is named 'api'
    path('', home),  # This handles requests to '/'
]
