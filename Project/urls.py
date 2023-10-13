from django.contrib import admin
from django.urls import path,include
from rest_framework.response import Response
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app.views import *
from rest_framework import status


urlpatterns = [
    path('test/',test,name="Testing"),
    path('admin/', admin.site.urls),
    path('',home,name='Home'),
    path('register/',UserAPI.as_view(),name='user-related'),
    path('handle/',HandleFileUpload),
    path('download/<str:uid>/',download,name='download-object'),
    path('user/',LoginAPI.as_view(),name='login api view'),
    path('logout/',Logout,name="Logging Out"),
    path('getlinks/',getLinks,name='getting all links of a user'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

urlpatterns+=staticfiles_urlpatterns()
