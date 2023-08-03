
from django.contrib import admin
from django.urls import path, include
from sd_support.views import ProjectViewset
from rest_framework import routers


urlpatterns = [
    path('admin/', admin.site.urls),



    #Authentication
    path('api-auth/', include('sd_accounts.urls')),

    #Token


    #Support API
    path('api/', include('sd_support.urls')),

]