from django.conf.urls import url, include
from django.urls import path, re_path
from . import views

app_name="reservation"

urlpatterns=[

    url(r'^listeReserv$', views.listReserv ,name="reservation"),

]
