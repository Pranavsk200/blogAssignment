from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
#from django.conf.url import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_api.urls')),
]
