from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index,name='index'),
    path('upload',views.upload,name='upload'),
    path('detection/logs',views.logs,name="logs"),
    path('detection/result/<id>',views.result,name="result"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)