
from django.contrib import admin
from django.urls import path, include 


urlpatterns = [
    path('',include('miapp.urls')),
    path('admin/', admin.site.urls),
    path('/',include('miapp.urls')),   
]
